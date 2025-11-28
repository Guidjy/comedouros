from ..models import Animal, Refeicao


def get_animais_e_refeicoes_com_lote(lote):
    animais = Animal.objects.filter(lote__nome=lote)
    if not animais.exists():
        animais = {'erro': f'Não foram encontrados animais no lote {lote}'}
    
    refeicoes = Refeicao.objects.filter(animal__lote__nome=lote)
        
    return animais, refeicoes