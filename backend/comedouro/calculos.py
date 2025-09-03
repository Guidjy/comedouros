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


def gera_comportamento_ingestivo(animal_id):
    """Gera um relatório do comportamento ingestivo de um animal

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

    # calcula consumo diário
    consumo_diario = []
    for refeicao in refeicoes:
        consumo_diario.append({f'{refeicao.data}': refeicao.consumo_kg})
        
    return consumo_diario
    
    