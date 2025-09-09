import numpy as np
from ..models import Animal, Refeicao


# comportamento ingestivo

def calcula_cmn_kg(peso_vivo_kg, cmn_porcentagem):
    """Cálculo do CMN(Kg)
    args:
    - peso vivo atual (Kg)
    - CMN %
    """
    return peso_vivo_kg * cmn_porcentagem


def calcula_min_por_refeicao(hora_entrada, hora_saida):
    """Calcula duração da refeição
    args:
    - horario de entrada
    - horario de saida
    """
    return hora_saida - hora_entrada


def gera_consumo_diario_animal(animal_id, data=None):
    """Gera um relatório do consumo diário total de um animal por dia, ou do consumo por refeição
    em um dia, se a data for especificada

    Args:
        - animal_id: id do animal a gerar relatório
        - data: restringe a visualização à um dia só
    """
    
    # busca o objeto do animal
    try:
        animal = Animal.objects.get(id=animal_id)
    except Animal.DoesNotExist as e:
        return {'erro': f'{e}'}
    
    # busca todas as refeições do animal da mais recente pra menos recente
    if data:
        refeicoes = Refeicao.objects.filter(animal=animal, data=data)
    else:
        refeicoes = Refeicao.objects.filter(animal=animal).order_by('data')
    if not refeicoes.exists():
        return {'erro': 'Não foram encontradas refeições realizadas por esse animal.'}

    if data is None:
        # adiciona o consumo de cada refeicao a um dicionário {'data': [consumo...]}
        refeicoes_por_dia = {}
        for refeicao in refeicoes:
            data = refeicao.data
            if f'{data}' not in refeicoes_por_dia:
                refeicoes_por_dia[f'{data}'] = []
            refeicoes_por_dia[f'{data}'].append(refeicao.consumo_kg)
        
        # calcula o total de consumo a cada dia
        consumo_diario = {}
        for dia, refeicao in refeicoes_por_dia.items():
            consumo_diario[f'{dia}'] = np.array(refeicao, dtype=float).sum()
    
    else:
        consumo_diario = []
        for refeicao in refeicoes:
            consumo_diario.append({f'{refeicao.horario_entrada}': refeicao.consumo_kg})
        
    return consumo_diario


def gera_consumo_diario_lote(lote_id, data=None):
    """Gera um relatório do consumo diário total de um lote por dia

    Args:
        lote_id: id do lote a gerar consumo por refeicao
    """
    
    # busca todos os animais do lote
    animais = Animal.objects.filter(lote=lote_id)
    if not animais.exists():
        return {'erro': f'Não foram encontrados animais no lote {lote_id}'}
        
    # percorre todos os animais do lote
    consumo_diario = {}  # {'aaaa-mm-dd': x(Kg)}
    
    if data is None:
        for animal in animais:
            # pega as refeições do animal
            refeicoes = Refeicao.objects.filter(animal=animal)
            # adiciona as refeições ao dicionário de consumo diário
            for refeicao in refeicoes:
                if f'{refeicao.data}' not in consumo_diario:
                    consumo_diario[f'{refeicao.data}'] = []
                consumo_diario[f'{refeicao.data}'].append(refeicao.consumo_kg)
        # calcula o consumo diário do lote
        for dia, consumo in consumo_diario.items():
            consumo_diario[f'{dia}'] = np.array(consumo, dtype=float).sum()
    
    else:
        for animal in animais:
            brinco_num = f'{animal.brinco.numero}'
            consumo_diario[brinco_num] = []
            refeicoes =  Refeicao.objects.filter(animal=animal, data=data)
            for refeicao in refeicoes:
                consumo_diario[brinco_num].append(refeicao.consumo_kg)
            consumo_diario[brinco_num] = np.array(consumo_diario[brinco_num], dtype=float).sum()
    
    return consumo_diario
        
        
            
        
    
