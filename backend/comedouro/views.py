from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *

from .utils.csv import le_relatorio_cocho
from .utils.queries import get_animais_e_refeicoes_com_lote
from .calculos import comportamento_ingestivo as ci
from .calculos import desempenho as dp
from .calculos import viabilidade as vb


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Operações CRUD
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


class LoteViewSet(viewsets.ModelViewSet):
    queryset = Lote.objects.all()
    serializer_class = LoteSerializer
    

class BrincoViewSet(viewsets.ModelViewSet):
    queryset = Brinco.objects.all()
    serializer_class = BrincoSerializer
    

class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['lote', 'raca', 'categoria']
    
    def retrieve(self, request, *args, **kwargs):
        # adiciona o peso atual a response
        animal = Animal.objects.get(id=kwargs.get('pk'))
        peso_atual = Refeicao.objects.filter(animal=animal).last().peso_vivo_entrada_kg
        # adiciona o número do brinco e tag_id do brinco a response
        response =  super().retrieve(request, *args, **kwargs)
        response.data['peso_atual'] = peso_atual
        response.data['brinco_numero'] = animal.brinco.numero
        response.data['brinco_tag_id'] = animal.brinco.tag_id
        return response
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        # pega todos ids do queryset
        qs = self.filter_queryset(self.get_queryset())
        for animal_dict, animal in zip(response.data, qs):
            refeicao = Refeicao.objects.filter(animal=animal).last()
            animal_dict["peso_atual"] = (
                refeicao.peso_vivo_entrada_kg if refeicao else None
            )
            animal_dict['brinco_numero'] = animal.brinco.numero
            animal_dict['brinco_tag_id'] = animal.brinco.tag_id
            
        return response
    
class RefeicaoViewSet(viewsets.ModelViewSet):
    queryset = Refeicao.objects.all()
    serializer_class = RefeicaoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['animal', 'data']
    ordering_fields = ['data']
    ordering = ['-data']  # default ordering
    

@api_view(['POST'])
def cria_animais_com_csv(request):
    """Cria animais a partir de um arquivo csv
    """
    print("FILES:", request.FILES)
    
    # lê os dados do csv
    arquivo = request.FILES.get('file')
    animais, refeicoes = le_relatorio_cocho(arquivo)
    
    # adiciona todos ao "lote_real_1" por enquanto
    try:
        lote = Lote.objects.get(nome="lote_real_1")
    except Lote.DoesNotExist:
        return Response({'erro': 'lote_real_1 não encontrado'}, status=status.HTTP_400_BAD_REQUEST)
    
    # adiciona os animais ao banco de dados
    tag_animal_map = {}
    for animal in animais:
        tag_id = animal['tag_id']
        numero = animal['numero']
        # cria ou pega o brinco
        brinco, criado = Brinco.objects.get_or_create(
            tag_id=tag_id,
            numero=numero
        )
        # cria ou pega o animal
        a, criado = Animal.objects.get_or_create(
            brinco=brinco,
            lote=lote
        )
        tag_animal_map[tag_id] = a
        
        
    # adiciona as refeições ao banco
    for refeicao in refeicoes:
        horario_entrada = refeicao['horario_entrada']
        horario_saida = refeicao['horario_saida']
        data = refeicao['data']
        consumo_kg = refeicao['consumo_kg']
        peso_vivo_entrada_kg = refeicao['peso_vivo_entrada_kg']
        tag_id = refeicao['tag_id']
        
        r, criado = Refeicao.objects.get_or_create(
            horario_entrada=horario_entrada,
            horario_saida=horario_saida,
            consumo_kg=consumo_kg,
            peso_vivo_entrada_kg=peso_vivo_entrada_kg,
            data=data,
            animal=tag_animal_map[tag_id]
        )
        
    return Response({'sucesso': 'Animais e refeições registradas com sucesso'}, status=status.HTTP_200_OK)
    

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Comportamento ingestivo
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


@api_view(['GET'])
def consumo_diario(request, animal_ou_lote, numero_ou_nome, data=None):
    """Gera um relatório do comportamento ingestivo do
    animal de id "animal_id".
    - Retorno:
        - consumo_diario: [{"dd-mm-aaaa": consumo_kg}]
    """
    # gera o consumo diário de um animal
    if animal_ou_lote == 'animal': 
        try:
            animal = Animal.objects.get(brinco__numero=numero_ou_nome)
        except Animal.DoesNotExist:
            return Response({'erro': f'Não existe um animal com um brinco de número {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)
        
        refeicoes = Refeicao.objects.filter(animal=animal)
        
        consumo_diario = ci.gera_consumo_diario_animal(animal, refeicoes, data)
        
        if 'erro' in consumo_diario:
            return Response(consumo_diario, status=status.HTTP_400_BAD_REQUEST)
        return Response(consumo_diario, status=status.HTTP_200_OK)
        
    # gera o consumo diário de um lote
    elif animal_ou_lote == 'lote':
        # busca todos os animais do lote
        animais, refeicoes = get_animais_e_refeicoes_com_lote(numero_ou_nome)
        if 'erro' in animais:
            return Response(animais, status=status.HTTP_400_BAD_REQUEST)
        
        consumo_diario = ci.gera_consumo_diario_lote(animais, refeicoes, data)
        
        if 'erro' in consumo_diario:
            return Response(consumo_diario, status=status.HTTP_400_BAD_REQUEST)
        return Response(consumo_diario, status=status.HTTP_200_OK)
    
    # erro 
    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def minuto_por_refeicao(request, animal_ou_lote, numero_ou_nome, data=None):
    if animal_ou_lote == 'animal':
        try:
            animal = Animal.objects.get(brinco__numero=numero_ou_nome)
        except Animal.DoesNotExist:
            return Response({'erro': f'Não existe um animal com um brinco de número {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)
        
        refeicoes = Refeicao.objects.filter(animal=animal)
        
        minuto_por_refeicao = ci.gera_minuto_por_refeicao_animal(animal, refeicoes, data)
            
    else:
        animais, refeicoes = get_animais_e_refeicoes_com_lote(numero_ou_nome)
        if 'erro' in animais:
            return Response(animais, status=status.HTTP_400_BAD_REQUEST)
        
        minuto_por_refeicao = ci.gera_minuto_por_refeicao_lote(animais, refeicoes, data)
    
    if 'erro' in minuto_por_refeicao:
        return Response(minuto_por_refeicao, status=status.HTTP_400_BAD_REQUEST)
    return Response(minuto_por_refeicao, status=status.HTTP_200_OK)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Desempenho
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


@api_view(['GET'])
def evolucao_peso_por_dia(request, animal_ou_lote, numero_ou_nome):
    """Gera um relatório da evolução do peso vivo de um animal

    Args:
        animal_ou_lote (str): string 'animal' ou 'lote' para decidir qual relatório gerar.
        numero_ou_nome (str): numero do brinco do animal ou nome do lote
    """
    
    # animal
    if animal_ou_lote == 'animal':
        try:
            animal = Animal.objects.get(brinco__numero=numero_ou_nome)
        except Animal.DoesNotExist:
            return Response({'erro': f'Não existe um animal com um brinco de número {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)
        
        refeicoes = Refeicao.objects.filter(animal=animal)
        if not refeicoes.exists():
            return Response({'erro': f'não foram encontradas refeições para o animal com o brinco {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)
        
        pesos = dp.calcula_evolucao_peso_por_dia_animal(refeicoes)
            
    # lote
    elif animal_ou_lote == 'lote':
        
        animais, refeicoes = get_animais_e_refeicoes_com_lote(numero_ou_nome)
        if 'erro' in animais:
            return Response(animais, status=status.HTTP_400_BAD_REQUEST)
        
        pesos = dp.calcula_evolucao_peso_por_dia_lote(refeicoes)
        
    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(pesos, status=status.HTTP_200_OK)


@api_view(['GET'])
def evolucao_consumo_diario(request, animal_ou_lote, numero_ou_nome):
    """Gera um relatório da evolução do consumo diário de um animal ou lote

    Args:
        animal_ou_lote (str): string 'animal' ou 'lote' para decidir qual relatório gerar.
        numero_ou_nome (str): numero do brinco do animal ou nome do lote
    """
    
    #animal
    if animal_ou_lote == 'animal':
        try:
            animal = Animal.objects.get(brinco__numero=numero_ou_nome)
        except Animal.DoesNotExist:
            return Response({'erro': f'Não existe um animal com um brinco de número {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)
        
        refeicoes = Refeicao.objects.filter(animal=animal)
        if not refeicoes.exists():
            return Response({'erro': f'não foram encontradas refeições para o animal de id {id}'}, status=status.HTTP_400_BAD_REQUEST)
        
        consumo = dp.calcula_evolucao_consumo_diario_animal(refeicoes)
    
    #lote
    elif animal_ou_lote == 'lote':
        animais, refeicoes = get_animais_e_refeicoes_com_lote(numero_ou_nome)
        if 'erro' in animais:
            return Response(animais, status=status.HTTP_400_BAD_REQUEST)
        
        consumo = dp.calcula_evolucao_consumo_diario_lote(refeicoes)
                
    # erro     
    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(consumo, status=status.HTTP_200_OK)


@api_view(['GET'])
def evolucao_ganho(request, animal_ou_lote, numero_ou_nome):
    """Gera um relatório da evolução de ganho de peso de um animal

    Args:
        animal_ou_lote (str): string 'animal' ou 'lote' para decidir qual relatório gerar.
        numero_ou_nome (str): numero do brinco do animal ou nome do lote
    """
    
    # animal
    if animal_ou_lote == 'animal':
        try:
            animal = Animal.objects.get(brinco__numero=numero_ou_nome)
        except Animal.DoesNotExist:
            return Response({'erro': f'Não existe um animal com um brinco de número {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)
        
        refeicoes = Refeicao.objects.filter(animal=animal)
        if not refeicoes.exists():
            return Response({'erro': f'Não existem refeições relacionadas ao animal de id {animal.id}'}, status=status.HTTP_400_BAD_REQUEST)
        elif len(refeicoes) < 2:
            return Response({'erro': f'Não existem refeições suficientes para calcular o ganho do animal de id {animal.id}'}, status=status.HTTP_400_BAD_REQUEST)
        
        ganho = dp.calcula_ganho_peso_animal(animal, refeicoes)
        
        if 'erro' in ganho:
            return Response(ganho, status=status.HTTP_400_BAD_REQUEST)
        
    elif animal_ou_lote == 'lote':
        animais, refeicoes = get_animais_e_refeicoes_com_lote(numero_ou_nome)
        if 'erro' in animais:
            return Response(animais, status=status.HTTP_400_BAD_REQUEST)
        
        ganho = dp.calcula_ganho_peso_lote(animais, refeicoes)
        if 'erro' in ganho:
            return Response(ganho, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(ganho, status=status.HTTP_200_OK)


@api_view(['GET'])
def evolucao_gmd(request, animal_ou_lote, numero_ou_nome):
    """Gera um relatório da evolução do GMD (ganho médio diário)

    Args:
        animal_ou_lote (str): string 'animal' ou 'lote' para decidir qual relatório gerar.
        numero_ou_nome (str): numero do brinco do animal ou nome do lote
    """
    
    #animal
    if animal_ou_lote == 'animal':
        try:
            animal = Animal.objects.get(brinco__numero=numero_ou_nome)
        except Animal.DoesNotExist:
            return Response({'erro': f'Não existe um animal com um brinco de número {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)
        
        refeicoes = Refeicao.objects.filter(animal=animal)
        if not refeicoes.exists():
            return Response({'erro': f'Não existem refeições relacionadas ao animal de id {animal.id}'}, status=status.HTTP_400_BAD_REQUEST)
        elif len(refeicoes) < 2:
            return Response({'erro': f'Não existem refeições suficientes para calcular o ganho do animal de id {animal.id}'}, status=status.HTTP_400_BAD_REQUEST)
        
        gmd = dp.calcula_gmd_animal(animal, refeicoes)
        if 'erro' in gmd:
            return Response(gmd, status=status.HTTP_400_BAD_REQUEST)
        
    elif animal_ou_lote == 'lote':
        animais, refeicoes = get_animais_e_refeicoes_com_lote(numero_ou_nome)
        if 'erro' in animais:
            return Response(animais, status=status.HTTP_400_BAD_REQUEST)
        
        gmd = dp.calcula_gmd_lote(animais, refeicoes)
        if 'erro' in gmd:
            return Response(gmd, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(gmd, status=status.HTTP_200_OK)
    

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Viabilidade
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


@api_view(['GET'])
def custo_total(request, animal_ou_lote, numero_ou_nome, preco_kg_racao):
    """Gera um relatório do custo total de ração de um animal ou de um lote.

    Args:
        animal_ou_lote (str): string 'animal' ou 'lote' para decidir qual relatório gerar.
        numero_ou_nome (str): numero do brinco do animal ou nome do lote
        preco_kg_racao (str): preço do kilograma da ração no formato 'x.y'
        
    Returns:
        custo_total: (float) custo total
    """
    preco_kg_racao = float(preco_kg_racao)
    
    if animal_ou_lote == 'animal':
        try:
            animal = Animal.objects.get(brinco__numero=numero_ou_nome)
        except Animal.DoesNotExist:
            return Response({'erro': f'Não existe um animal com um brinco de número {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)
        
        refeicoes = Refeicao.objects.filter(animal=animal)
        if not refeicoes.exists():
            return Response({'erro': f'Não existem refeições relacionadas ao animal de id {animal.id}'}, status=status.HTTP_400_BAD_REQUEST)
        
        custo_total = vb.calcula_custo_total_animal(refeicoes, preco_kg_racao)
        
        return Response({'custo_total': round(custo_total, 2)}, status=status.HTTP_200_OK)
    
    elif animal_ou_lote == 'lote':
        animais = Animal.objects.filter(lote__nome=numero_ou_nome)
        if not animais.exists():
            return Response({'erro': f'não foram encontrados animais para o lote de id {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)

        custo_total = vb.calcula_custo_total_lote(animais, preco_kg_racao)
            
        return Response({'custo_total': round(custo_total, 2)}, status=status.HTTP_200_OK)
    
    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def evolucao_custo_diario(request, animal_ou_lote, numero_ou_nome, preco_kg_racao):
    """Gera um relatório do custo total de ração de um animal ou de um lote.

    Args:
        animal_ou_lote (str): string 'animal' ou 'lote' para decidir qual relatório gerar.
        numero_ou_nome (str): numero do brinco do animal ou nome do lote
        preco_kg_racao (str): preço do kilograma da ração no formato 'x.y'

    Returns:
        [aaaa--mm-dd: (float) custo no dia]
    """
    
    preco_kg_racao = float(preco_kg_racao)
    
    if animal_ou_lote == 'animal':
        try:
            animal = Animal.objects.get(brinco__numero=numero_ou_nome)
        except Animal.DoesNotExist:
            return Response({'erro': f'Não existe um animal com um brinco de número {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)
        
        refeicoes = Refeicao.objects.filter(animal=animal)
        if not refeicoes.exists():
            return Response({'erro': f'Não existem refeições relacionadas ao animal de id {animal.id}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # calcula o custo de um animal em um dia e adiciona a um dicionário
        evolucao_custo = vb.calcula_evolucao_custo_diario_animal(refeicoes, preco_kg_racao)
        
        return Response(evolucao_custo, status=status.HTTP_200_OK)
    
    elif animal_ou_lote == 'lote':
        animais, refeicoes = get_animais_e_refeicoes_com_lote(numero_ou_nome)
        if 'erro' in animais:
            return Response(animais, status=status.HTTP_400_BAD_REQUEST)
        
        # calcula o custo de um lote em um dia e adiciona a um dicionário
        evolucao_custo = vb.calcula_evolucao_custo_diario_lote(animais, refeicoes, preco_kg_racao)
            
        return Response(evolucao_custo, status=status.HTTP_200_OK)
    
    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def ganho_por_dia(request, animal_ou_lote, numero_ou_nome, reais_por_kg_de_peso_vivo):
    """Gera um relatório do ganho por dia em reais de um animal ou de um lote.

    Args:
        animal_ou_lote (str): string 'animal' ou 'lote' para decidir qual relatório gerar.
        numero_ou_nome (str): numero do brinco do animal ou nome do lote
        reais_por_kg_de_peso_vivo (str): preço do kilograma de peso vivo de um animal (formato x.y)

    Returns:
        aaaa--mm-dd: (float) custo no dia
    """
    reais_por_kg_de_peso_vivo = float(reais_por_kg_de_peso_vivo)
    
    if animal_ou_lote == 'animal':
        try:
            animal = Animal.objects.get(brinco__numero=numero_ou_nome)
        except Animal.DoesNotExist:
            return Response({'erro': f'Não existe um animal com um brinco de número {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)
        
        refeicoes = Refeicao.objects.filter(animal=animal)
        if not refeicoes.exists():
            return Response({'erro': f'Não existem refeições relacionadas ao animal de id {animal.id}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # ganho por dia = GMD * reais/kg_pv
        ganho_por_dia = vb.calcula_ganho_por_dia_animal(animal, refeicoes, reais_por_kg_de_peso_vivo)
        
        return Response(ganho_por_dia, status=status.HTTP_200_OK)
    
    elif animal_ou_lote == 'lote':
        animais, refeicoes = get_animais_e_refeicoes_com_lote(numero_ou_nome)
        if 'erro' in animais:
            return Response(animais, status=status.HTTP_400_BAD_REQUEST)
        
        ganho_por_dia = vb.calcula_ganho_por_dia_lote(animais, refeicoes, reais_por_kg_de_peso_vivo)
            
        return Response(ganho_por_dia, status=status.HTTP_200_OK)  

    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)
    

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Relatório Geral
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


@api_view(['GET'])
def relatorio_geral(request, animal_ou_lote, numero_ou_nome, preco_kg_racao, reais_por_kg_de_peso_vivo):
    """Gera um relatório geral de todos os grafos para um animal

    Args:
        animal_ou_lote (str): string 'animal' ou 'lote' para decidir qual relatório gerar.
        numero_ou_nome (str): numero do brinco do animal ou nome do lote
        preco_kg_racao (str): preço do kilograma da ração  (formato x.y)
        reais_por_kg_de_peso_vivo (str): preço do kilograma de peso vivo de um animal (formato x.y)
    """
    
    preco_kg_racao = float(preco_kg_racao)
    reais_por_kg_de_peso_vivo = float(reais_por_kg_de_peso_vivo)
    relatorio = {}
    
    if animal_ou_lote == 'animal':
        try:
            animal = Animal.objects.get(brinco__numero=numero_ou_nome)
        except Animal.DoesNotExist:
            return Response({'erro': f'Não existe um animal com um brinco de número {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)
        
        refeicoes = Refeicao.objects.filter(animal=animal)
        if not refeicoes.exists():
            return Response({'erro': f'não foram encontradas refeições para o animal com o brinco {numero_ou_nome}'}, status=status.HTTP_400_BAD_REQUEST)
        
        relatorio['consumo_diario'] = ci.gera_consumo_diario_animal(animal, refeicoes)
        relatorio['minuto_por_refeicao'] = ci.gera_minuto_por_refeicao_animal(animal, refeicoes)
        relatorio['evolucao_peso_por_dia'] = dp.calcula_evolucao_peso_por_dia_animal(refeicoes)
        relatorio['evolucao_consumo_diario'] = dp.calcula_evolucao_consumo_diario_animal(refeicoes)
        relatorio['evolucao_ganho'] = dp.calcula_ganho_peso_animal(animal, refeicoes)
        relatorio['evolucao_gmd'] = dp.calcula_gmd_animal(animal, refeicoes)
        relatorio['custo_total'] = vb.calcula_custo_total_animal(refeicoes, preco_kg_racao)
        relatorio['evolucao_custo_diario'] = vb.calcula_evolucao_custo_diario_animal(refeicoes, preco_kg_racao)
        relatorio['ganho_por_dia'] = vb.calcula_ganho_por_dia_animal(animal, refeicoes, reais_por_kg_de_peso_vivo)
        
        return Response(relatorio, status=status.HTTP_200_OK)
    
    elif animal_ou_lote == 'lote':
        
        if numero_ou_nome == 'TODOS':
            animais = Animal.objects.all()
            refeicoes = Refeicao.objects.all()
        else:
            animais, refeicoes = get_animais_e_refeicoes_com_lote(numero_ou_nome)
            if 'erro' in animais:
                return Response(animais, status=status.HTTP_400_BAD_REQUEST)
        
        relatorio['consumo_diario'] = ci.gera_consumo_diario_lote(animais, refeicoes)
        relatorio['minuto_por_refeicao'] = ci.gera_minuto_por_refeicao_lote(animais, refeicoes)
        relatorio['evolucao_peso_por_dia'] = dp.calcula_evolucao_peso_por_dia_lote(refeicoes)
        relatorio['evolucao_consumo_diario'] = dp.calcula_evolucao_consumo_diario_lote(refeicoes)
        relatorio['evolucao_ganho'] =  dp.calcula_ganho_peso_lote(animais, refeicoes)
        relatorio['evolucao_gmd'] = dp.calcula_gmd_lote(animais, refeicoes)
        relatorio['custo_total'] = vb.calcula_custo_total_lote(animais, preco_kg_racao)
        relatorio['evolucao_custo_diario'] = vb.calcula_evolucao_custo_diario_lote(animais, refeicoes, preco_kg_racao)
        relatorio['ganho_por_dia'] = vb.calcula_ganho_por_dia_lote(animais, refeicoes, reais_por_kg_de_peso_vivo)
        
        return Response(relatorio, status=status.HTTP_200_OK)
    
    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)
    