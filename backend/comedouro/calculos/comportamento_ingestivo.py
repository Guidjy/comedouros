import numpy as np
from ..models import Animal, Refeicao
from datetime import datetime


# comportamento ingestivo


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
        
        
def calcula_duracao_refeicao(refeicao):
    """Retorna a duração de uma refeição em minutos"""
    hoje = datetime.today().date()
    horario_entrada = datetime.combine(hoje, refeicao.horario_entrada)
    horario_saida = datetime.combine(hoje, refeicao.horario_saida)
    duracao = horario_saida - horario_entrada
    duracao = duracao.total_seconds() / 60
    
    return duracao

        
def gera_minuto_por_refeicao_animal(animal_id, data=None):
    """Gera um relatório da quantidade de minutos por refeição de um animal. Se um dia for
    passado por argumento, são retornados os tempos exatos de cada refeição naquele dia, se não,
    calcula-se a média das durações das refeições para cada dia.

    Args:
        animal_id: id do animal
        data: data
    """
    try:
        animal = Animal.objects.get(id=animal_id)
    except Animal.DoesNotExist:
        return {'erro': f'Não existe um animal com o id {animal_id}'}
    
    minuto_por_refeicao = {}
    
    if data is not None:
        # pega as refeições do animal
        refeicoes = Refeicao.objects.filter(animal=animal, data=data)
        if not refeicoes.exists():
            return {'erro': f'Não foram encontradas refeições para o animal de id {animal_id}'}
        # adiciona as refeições a um dicionário {'número da refeição': duração}
        i = 1
        for refeicao in refeicoes:
            minuto_por_refeicao[f'refeicao_n{i}'] = calcula_duracao_refeicao(refeicao)
            i += 1
        
    else:
        # pega as refeições do animal
        refeicoes = Refeicao.objects.filter(animal=animal)
        if not refeicoes.exists():
            return {'erro': f'Não foram encontradas refeições para o animal de id {animal_id}'}
        # adiciona as refeições ao dicionário {'data': [duração_refeição1, duração_refeição2...]}
        for refeicao in refeicoes:
            duracao = calcula_duracao_refeicao(refeicao)
            data = refeicao.data
            if f'{data}' not in minuto_por_refeicao:
                minuto_por_refeicao[f'{data}'] = []
            minuto_por_refeicao[f'{data}'].append(duracao)
        # calcula a média da duração das refeições a cada dia
        for dia, duracao in minuto_por_refeicao.items():
            minuto_por_refeicao[dia] = np.array(minuto_por_refeicao[dia], dtype=float).mean()
        
    return minuto_por_refeicao
    

def gera_minuto_por_refeicao_lote(lote_id):
    """Gera um relatório da quantidade de minutos por refeição de um lote. Se um dia for
    passado por argumento, são retornados as medias de duração de cada refeição naquele dia, se não,
    calcula-se a média das durações das refeições para cada dia.

    Args:
        lote_id: id do animal
        data: data
    """
    animais = Animal.objects.filter(lote=lote_id)
    if not animais.exists():
        return {'erro': f'Não foram encontrados animais para o lote {lote_id}'}
    
    minutos_por_refeicao = {}
    
    for animal in animais:
        refeicoes = Refeicao.objects.filter(animal=animal)
        for refeicao in refeicoes:
            data = refeicao.data
            if f'{data}' not in minutos_por_refeicao:
                minutos_por_refeicao[f'{data}'] = []
            duracao = calcula_duracao_refeicao(refeicao)
            minutos_por_refeicao[f'{data}'].append(duracao)
    
    for data, refeicao in minutos_por_refeicao.items():
        minutos_por_refeicao[f'{data}'] = np.array(minutos_por_refeicao[f'{data}'], dtype=float).mean()
    
    return minutos_por_refeicao
    