from ..models import Animal, Refeicao
from . import desempenho as dp


def calcula_custo_total_animal(refeicoes, preco_kg_racao):
    custo_total = 0
    for refeicao in refeicoes:
        custo_total += refeicao.consumo_kg * preco_kg_racao
        
    return custo_total


def calcula_evolucao_custo_diario_animal(refeicoes, preco_kg_racao):
    evolucao_custo = {}
    for refeicao in refeicoes:
        data = refeicao.data
        if f'{data}' not in evolucao_custo:
            evolucao_custo[f'{data}'] = 0
        evolucao_custo[f'{data}'] += round(refeicao.consumo_kg * preco_kg_racao, 2)
        
    return evolucao_custo


def calcula_ganho_por_dia_animal(animal, refeicoes, reais_por_kg_de_peso_vivo):
    # ganho por dia = GMD * reais/kg_pv
    gmd = dp.calcula_gmd_animal(animal, refeicoes)
    ganho_por_dia = {}
    for data, ganho in gmd.items():
        ganho_por_dia[f'{data}'] = ganho * reais_por_kg_de_peso_vivo
        ganho_por_dia[f'{data}'] = round(ganho_por_dia[f'{data}'], 2)
        
    return ganho_por_dia