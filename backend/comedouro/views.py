from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *

from .utils.csv import le_relatorio_cocho
from .calculos import comportamento_ingestivo as ci
from .calculos import desempenho as dp


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
        response =  super().retrieve(request, *args, **kwargs)
        response.data['peso_atual'] = peso_atual
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
    arquivo = request.FILES.get('arquivo')
    animais, refeicoes = le_relatorio_cocho(arquivo)
    
    # adiciona os animais e refeições ao banco de dados
    tag_dos_animais = {}
    lote = Lote.objects.get(id=2)
    for tag_id, numero in animais.items():
        print(f'{tag_id}: {numero}')
        # cria ou pega o brinco
        brinco, _ = Brinco.objects.get_or_create(
            tag_id=tag_id,
            defaults={'numero': numero}
        )
        # cria ou pega oanimal
        animal, _ = Animal.objects.get_or_create(
            brinco=brinco,
            defaults={'lote': lote}
        )
        tag_dos_animais[f'{tag_id}'] = animal
        
        
    for refeicao in refeicoes:
        animal = tag_dos_animais[f'{refeicao['animal']}']
        
        refeicao, _ = Refeicao.objects.get_or_create(
            horario_entrada=refeicao['horario_entrada'],
            horario_saida=refeicao['horario_saida'],
            consumo_kg=refeicao['consumo_kg'],
            peso_vivo_entrada_kg=refeicao['peso_vivo_entrada_kg'],
            data=refeicao['data'],
            animal=animal
        )
    
    
    return Response({'sucesso': 'Animais e refeições registradas com sucesso'}, status=status.HTTP_200_OK)
    

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Comportamento ingestivo
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


@api_view(['GET'])
def consumo_diario(request, animal_ou_lote, id, data=None):
    """Gera um relatório do comportamento ingestivo do
    animal de id "animal_id".
    - Retorno:
        - consumo_diario: [{"dd-mm-aaaa": consumo_kg}]
    """
    # gera o consumo diário de um animal
    if animal_ou_lote == 'animal': 
        if data is None:
            consumo_diario = ci.gera_consumo_diario_animal(id)
        else:
            consumo_diario = ci.gera_consumo_diario_animal(id, data)
        
        if 'erro' in consumo_diario:
            return Response(consumo_diario, status=status.HTTP_400_BAD_REQUEST)
        return Response(consumo_diario, status=status.HTTP_200_OK)
        
    # gera o consumo diário de um lote
    elif animal_ou_lote == 'lote':
        if data is None:
            consumo_diario = ci.gera_consumo_diario_lote(id)
        else:
            consumo_diario = ci.gera_consumo_diario_lote(id, data)
        if 'erro' in consumo_diario:
            return Response(consumo_diario, status=status.HTTP_400_BAD_REQUEST)
        return Response(consumo_diario, status=status.HTTP_200_OK)
    
    # erro 
    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def minuto_por_refeicao(request, animal_ou_lote, id, data=None):
    if animal_ou_lote == 'animal':
        if data is not None:
            minuto_por_refeicao = ci.gera_minuto_por_refeicao_animal(id, data)
        else:
            minuto_por_refeicao = ci.gera_minuto_por_refeicao_animal(id)
    else:
        minuto_por_refeicao = ci.gera_minuto_por_refeicao_lote(id)
    
    if 'erro' in minuto_por_refeicao:
        return Response(minuto_por_refeicao, status=status.HTTP_400_BAD_REQUEST)
    return Response(minuto_por_refeicao, status=status.HTTP_200_OK)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Desempenho
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


@api_view(['GET'])
def evolucao_peso_por_dia(request, animal_id):
    """Gera um relatório da evolução do peso vivo de um animal

    Args:
        animal_id: id do animal
    """
    
    try:
        animal = Animal.objects.get(id=animal_id)
    except Animal.DoesNotExist:
        return Response({'erro': f'animal com id {animal_id} não existe'}, status=status.HTTP_400_BAD_REQUEST)
    
    refeicoes = Refeicao.objects.filter(animal=animal)
    if not refeicoes.exists():
        return Response({'erro': f'não foram encontradas refeições para o animal de id {animal_id}'}, status=status.HTTP_400_BAD_REQUEST)
    
    pesos = {}
    for refeicao in refeicoes:
        pesos[f'{refeicao.data}'] = refeicao.peso_vivo_entrada_kg
        
    return Response(pesos, status=status.HTTP_200_OK)


@api_view(['GET'])
def evolucao_consumo_diario(request, animal_ou_lote, id):
    """Gera um relatório da evolução do consumo diário de um animal ou lote

    Args:
        id (int): id do animal ou lote a gerar o relatório
    """
    
    #animal
    if animal_ou_lote == 'animal':
        try:
            animal = Animal.objects.get(id=id)
        except Animal.DoesNotExist:
            return Response({'erro': f'animal com id {id} não existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        refeicoes = Refeicao.objects.filter(animal=animal)
        if not refeicoes.exists():
            return Response({'erro': f'não foram encontradas refeições para o animal de id {id}'}, status=status.HTTP_400_BAD_REQUEST)
        
        consumo = {}
        for refeicao in refeicoes:
            data = refeicao.data
            if f'{data}' not in consumo:
                consumo[f'{data}'] = 0
            consumo[f'{data}'] += refeicao.consumo_kg
    
    #lote
    elif animal_ou_lote == 'lote':
        animais = Animal.objects.filter(lote=id)
        if not animais.exists():
            return Response({'erro': f'não foram encontrados animais para o lote de id {id}'}, status=status.HTTP_400_BAD_REQUEST)
        
        consumo = {}
        for animal in animais:
            refeicoes = Refeicao.objects.filter(animal=animal)
            for refeicao in refeicoes:
                data = refeicao.data
                if f'{data}' not in consumo:
                    consumo[f'{data}'] = 0
                consumo[f'{data}'] += refeicao.consumo_kg
                
    # erro     
    else:
        return Response({'erro': f'argumento invárlido "{animal_ou_lote}"'}, status=status.HTTP_400_BAD_REQUEST)
        
    return Response(consumo, status=status.HTTP_200_OK)


@api_view(['GET'])
def evolucao_ganho(request, animal_id):
    """Gera um relatório da evolução de ganho de peso de um animal

    Args:
        animal_id (int): id do animal
    """
    try:
        animal = Animal.objects.get(id=animal_id)
    except Animal.DoesNotExist:
        return Response({'erro': f'Não existe um animal com o id {animal_id}'}, status=status.HTTP_400_BAD_REQUEST)
    
    ganho = dp.calcula_ganho_peso_animal(animal)
    if 'erro' in ganho:
        return Response(ganho, status=status.HTTP_400_BAD_REQUEST)
    return Response(ganho, status=status.HTTP_200_OK)


@api_view(['GET'])
def evolucao_gmd(request, animal_id):
    """Gera um relatório da evolução do GMD (ganho médio diário)

    Args:
        animal_id (int): id do animal
    """
    try:
        animal = Animal.objects.get(id=animal_id)
    except Animal.DoesNotExist:
        return Response({'erro': f'Não existe um animal com o id {animal_id}'}, status=status.HTTP_400_BAD_REQUEST)
    
    gmd = dp.calcula_gmd_animal(animal)
    if 'erro' in gmd:
        return Response(gmd, status=status.HTTP_400_BAD_REQUEST)
    return Response(gmd, status=status.HTTP_200_OK)
    
    
        
    