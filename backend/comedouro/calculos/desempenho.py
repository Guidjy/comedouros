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
            
        
    
            
        
        
    
    
    
    