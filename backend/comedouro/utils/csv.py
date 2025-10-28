import numpy as np
import pandas as pd


def le_relatorio_cocho(relatorio):
    """
    Retorna um dicionário com os animais e refeições do relatório
    
    args: 
        relatorio: arquivo csv
        
    retorno
        [animais, refeicoes]
    """
    
    animais = []    # lista de dicionários com os dados dos animais
    refeicoes = []  # lista de dicionários com os dados de uma refeição de um animal
    
    # abre o csv para leitura
    data_frame = pd.read_csv(relatorio)
    
    # percorre todas as linhas do csv
    i = 0
    for indice, linha in data_frame.iterrows():
        
        # registra os animais
        tag_id = linha['tag_id']
        numero = linha['nome']
        # verifica se um animal com essa tag_id de brinco ja foi adicionado à lista, e se não, adiciona a ela
        for animal in animais:
            if animal['tag_id'] == tag_id:
                break
        else:
            animal = {'tag_id': tag_id, 'numero': numero}
            animais.append(animal)
            i += 1
            
        # registra as refeições
        data, horario_entrada = linha['hora_entrada'].split()
        data, horario_saida = linha['hora_saida'].split()
        peso_vivo_entrada_kg = linha['peso_animal']
        consumo_kg = linha['peso_racao']
        
        # trata os erros de registro
        # -1: Leitura inválida da balança ou peso com varianã de 20% do anterior
        if peso_vivo_entrada_kg == -1:
            # tenta pegar o próximo peso válido do mesmo animal
            idx = data_frame.index.get_loc(indice)
            for next_idx in range(idx + 1, len(data_frame)):
                next_row = data_frame.iloc[next_idx]
                if next_row['tag_id'] == tag_id and next_row['peso_animal'] != -1:
                    peso_vivo_entrada_kg = next_row['peso_animal']
                    peso_vivo_entrada_kg = float(peso_vivo_entrada_kg)
                    break
            # se não encontrou peso válido, peso_vivo_entrada_kg permanece -1
            
        # -2: comedouro bloqueado
        if consumo_kg == -2:
            # tenta pegar o próximo valor válido do mesmo animal
            idx = data_frame.index.get_loc(indice)
            for next_idx in range(idx + 1, len(data_frame)):
                next_row = data_frame.iloc[next_idx]
                if next_row['tag_id'] == tag_id and next_row['peso_racao'] != -2:
                    consumo_kg = next_row['peso_racao']
                    consumo_kg = float(consumo_kg)
                    break
            # se não encontrou valor válido, consumo_kg permanece -2
        
        refeicao = {'horario_entrada': horario_entrada,
                    'horario_saida': horario_saida,
                    'data': data,
                    'consumo_kg': consumo_kg,
                    'peso_vivo_entrada_kg': peso_vivo_entrada_kg,
                    'tag_id': tag_id}
        refeicoes.append(refeicao)
        
    return animais, refeicoes
        
        
        
      