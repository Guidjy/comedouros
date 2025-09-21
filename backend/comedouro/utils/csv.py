import numpy as np
import pandas as pd


def le_relatorio_cocho(relatorio):
    """Retorna um dicionário com os animais e refeições do relatório
    """
    data_frame = pd.read_csv(relatorio)
    
    # lê os animais e refeicoes e adiciona a uma lista
    i = 0
    animais = {}
    refeicoes = []
    for indice, linha in data_frame.iterrows():
        # animal
        if f'{linha['tag_id']}' not in animais:
            animais[f'{linha['tag_id']}'] = 53 + i
            i += 1
        
        # refeição
        # pega os horários de entrada e saída e a data
        data, horario_entrada = linha['hora_entrada'].split()
        data, horario_saida = linha['hora_saida'].split()
        # pega o peso de entrada e o consumo
        peso_vivo_entrada_kg = linha['peso_animal']
        if (peso_vivo_entrada_kg == -1):
            continue
        peso_vivo_entrada_kg /= 1000
        peso_vivo_entrada_kg = round(peso_vivo_entrada_kg, 2)
        consumo_kg = round(linha['peso_racao'] / 1000, 2)
        
        refeicao = {
            'horario_entrada': horario_entrada,
            'horario_saida': horario_saida,
            'consumo_kg': consumo_kg,
            'peso_vivo_entrada_kg': peso_vivo_entrada_kg,
            'data': data,
            'animal': linha['tag_id']
        }
        refeicoes.append(refeicao)
        
    
    return animais, refeicoes