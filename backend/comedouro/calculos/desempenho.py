import numpy as np
from ..models import Animal, Refeicao


def calcula_ganho_peso_animal(animal):
    """Calcula o ganho de peso diário de um animal ao longo de toda sua vida.

    Args:
        animal (obj): objeto do animal
    """
    
    refeicoes = Refeicao.objects.filter(animal=animal)
    if not refeicoes.exists():
        return {'erro': f'Não existem refeições relacionadas ao animal de id {animal.id}'}
    elif len(refeicoes) < 2:
        return {'erro': f'Não existem refeições suficientes para calcular o ganho do animal de id {animal.id}'}
    
    peso_inicial = refeicoes[0].peso_vivo_entrada_kg
    primeiro_dia = refeicoes[0].data
    ganho = {}
    for refeicao in refeicoes:
        data = refeicao.data
        if data == primeiro_dia:
            continue
        ganho[f'{data}'] = round(refeicao.peso_vivo_entrada_kg - peso_inicial, 2)
    
    return ganho


def calcula_ganho_peso_lote(animais):
    """Calcula o ganho de peso diário de um lote ao longo de toda sua vida.

    Args:
        animais ([obj]): lista de animais
    """
    ganho = {}
    
    for animal in animais:
        refeicoes = Refeicao.objects.filter(animal=animal)
        peso_inicial = refeicoes[0].peso_vivo_entrada_kg
        primeiro_dia = refeicoes[0].data
        
        for refeicao in refeicoes:
            data = refeicao.data
            if data == primeiro_dia:
                continue
            if f'{data}' not in ganho:
                ganho[f'{data}'] = 0
            ganho[f'{data}'] += round(refeicao.peso_vivo_entrada_kg - peso_inicial, 2)
            
    return ganho
    

def calcula_gmd_animal(animal):
    """Calcula o GMD de um animal ao longo de toda sua vida

    Args:
        animal (obj): objeto do animal
    """
    
    refeicoes = Refeicao.objects.filter(animal=animal)
    if not refeicoes.exists():
        return {'erro': f'Não existem refeições relacionadas ao animal de id {animal.id}'}
    elif len(refeicoes) < 2:
        return {'erro': f'Não existem refeições suficientes para calcular o gmd do animal de id {animal.id}'}
    
    pesos = {}
    for refeicao in refeicoes:
        pesos[f'{refeicao.data}'] = refeicao.peso_vivo_entrada_kg
        
    gmd = {}
    dias = list(pesos.keys())
    pesos = list(pesos.values())
    soma_dos_ganhos = 0
    for i in range(1, len(dias)):
        soma_dos_ganhos += pesos[i] - pesos[i-1]
        gmd[f'{dias[i]}'] = round(soma_dos_ganhos / i, 2)
    
    return gmd


def calcula_gmd_lote(animais):
    """Calcula o GMD de um lote

    Args:
        animais ([obj]): lista de animais
    """
    
    gmd = {}
    for animal in animais:
        refeicoes = Refeicao.objects.filter(animal=animal)
        if not refeicoes.exists():
            return {'erro': f'Não existem refeições relacionadas ao animal de id {animal.id}'}
        elif len(refeicoes) < 2:
            return {'erro': f'Não existem refeições suficientes para calcular o gmd do animal de id {animal.id}'}
        
        pesos = {}
        for refeicao in refeicoes:
            pesos[f'{refeicao.data}'] = refeicao.peso_vivo_entrada_kg
            
        dias = list(pesos.keys())
        pesos = list(pesos.values())
        soma_dos_ganhos = 0
        for i in range(1, len(dias)):
            soma_dos_ganhos += pesos[i] - pesos[i-1]
            if f'{dias[i]}' not in gmd:
                gmd[f'{dias[i]}'] = 0
            gmd[f'{dias[i]}'] += soma_dos_ganhos / i
            gmd[f'{dias[i]}'] = round(gmd[f'{dias[i]}'], 2)
    
    return gmd
            
        
    
            
        
        
    
    
    
    