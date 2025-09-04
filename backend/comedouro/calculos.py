import numpy as np
from .models import Animal, Refeicao


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


def gera_consumo_diario_animal(animal_id):
    """Gera um relatório do consumo diário de um animal

    Args:
        animal_id: id do animal a gerar relatório
    """
    
    # busca o objeto do animal
    try:
        animal = Animal.objects.get(id=animal_id)
    except Animal.DoesNotExist as e:
        return {'erro': f'{e}'}
    
    # busca todas as refeições do animal da mais recente pra menos recente
    refeicoes = Refeicao.objects.filter(animal=animal).order_by('data')
    if not refeicoes.exists():
        return {'erro': 'Não foram encontradas refeições realizadas por esse animal.'}

    # adiciona o consumo de cada refeicao a um dicionário {'data': [consumo...]}
    refeicoes_por_dia = {}
    for refeicao in refeicoes:
        data = refeicao.data
        if f'{data}' not in refeicoes_por_dia:
            refeicoes_por_dia[f'{data}'] = []
        refeicoes_por_dia[f'{data}'].append(refeicao.consumo_kg)
    
    # calcula a média de consumo a cada dia
    consumo_diario = {}
    for dia, refeicao in refeicoes_por_dia.items():
        consumo_diario[f'{dia}'] = np.array(refeicao, dtype=float).mean()
        
    return consumo_diario


def gera_consumo_diario_lote(lote_id):
    """Gera um relatório da média do consumo por refeição dos animais de um lote

    Args:
        lote_id: id do lote a gerar consumo por refeicao
    """
    
    # busca todos os animais do lote
    animais = Animal.objects.filter(lote=lote_id)
    if not animais.exists():
        return {'erro': f'Não foram encontrados animais no lote {lote_id}'}
        
    # percorre todos os animais do lote
    consumo_diario_lote = {}  # dicionário onde serão guardados os pares {'animal': média_diária_animal}
    for animal in animais:
        
        # percorre todas as refeições de um animal
        refeicoes_por_dia_animal = {}
        refeicoes = Refeicao.objects.filter(animal=animal).order_by('data')
        for refeicao in refeicoes:
            
            # adiciona o consumo da refeição a um dicionário {'dia': [consumo_refeicao...]}
            data = refeicao.data
            if f'{data}' not in refeicoes_por_dia_animal:
                refeicoes_por_dia_animal[f'{data}'] = []
            refeicoes_por_dia_animal[f'{data}'].append(refeicao.consumo_kg)

        # calcula a média de consumo diário desse animal
        media = 0
        for dia, refeicoes in refeicoes_por_dia_animal.items():
            # calcula a média de um dia
            media += np.array(refeicoes, dtype=float).mean()
        # calcula a média entre todos os dias
        media /= len(refeicoes_por_dia_animal)
        
        consumo_diario_lote[f'{animal.animal_id_c}'] = media
        
        
    return consumo_diario_lote
            
        
    
    