import requests
import os
import hashlib
import time
from termcolor import colored
from datetime import datetime


def tem_internet(url="https://www.google.com", timeout=3):
    """Verifica se o dispositivo tem acesso a internet

    Args:
        url (str, optional): Defaults to "https://www.google.com".
        timeout (int, optional): Defaults to 3.

    Returns:
        bool
    """
    try:
        requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False


def hash_arquivo(caminho):
    """Calcula o hash MD5 do arquivo CSV"""
    with open(caminho, "rb") as f:
        # lê todos os bytes do arquivo e escreve na memória para depois calcular o hash MD5 desses bytes
        return hashlib.md5(f.read()).hexdigest() 


def main():
    api_url = 'http://127.0.0.1:8000/'
    diretorio_atual = os.path.dirname(__file__)
    caminho_arquivo = os.path.join(diretorio_atual, 'relatorio_cocho.csv')

    # hash's dos dados do arquivo .csv. Usados para verificar se houveram mudanças no arquivo
    hash_antigo = hash_arquivo(caminho_arquivo)
    sincronizado = True
    
    print('-=-=-=-=-=- Monitoramento de sincronização -=-=-=-=-=-')
        
    # laço principal da sincronização
    while True:
        agora = datetime.now()
        print(agora.strftime('> [%Y-%m-%d %H:%M:%S]'))
        time.sleep(5)  # evita uso desnecessário do cpu. Alterar intervalo se quizer sincronizações mais ou menos frequentes
        
        # verifica se houveram mudanças no arquivo
        try:
            hash_atual = hash_arquivo(caminho_arquivo)
        except FileNotFoundError:
            print(colored('> Arquivo CSV não encontrado.', 'red'))
            continue
        if hash_atual != hash_antigo:
            print('> Mudanças detectadas no arquivo.')
            sincronizado = False
            hash_antigo = hash_atual
        else:
            if sincronizado:
                print('> Não foram detectadas mudanças no arquivo...')
        
        # sincroniza as mudanças se tiver internet
        if not sincronizado:
            if tem_internet():
                print('> Internet detectada. Tentando sincronizar...')
            else:
                print('> Internet não detectada. Tentando novamente...')
                continue
            
            with open(caminho_arquivo, 'rb') as arquivo:
                arquivo_requisicao = {'file': (os.path.basename(caminho_arquivo), arquivo, 'text/csv')}
                try:
                    response = requests.post(f'{api_url}cria-animais-com-csv/', files=arquivo_requisicao)
                    if response.ok:
                        sincronizado = True
                        print(colored('> Sincronização bem-sucedida.', 'green'))
                    else:
                        print(colored(f'> Erro na sincronização: {response.status_code}', 'red'))
                except requests.RequestException as e:
                    print(colored(f'> Falha na conexão: {e}', 'red'))


if __name__ == '__main__':
    main()