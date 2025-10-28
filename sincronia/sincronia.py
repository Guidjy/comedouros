import requests
import os

api_url = 'http://127.0.0.1:8000/'
diretorio_atual = os.path.dirname(__file__)
caminho_arquivo = os.path.join(diretorio_atual, 'relatorio_cocho.csv')

# abre o arquivo no modo leitura binária (requisição precisa dos dados binários do arquivo)
with open(caminho_arquivo, 'rb') as arquivo:
    arquivo_requisicao = {'file': (os.path.basename(caminho_arquivo), arquivo, 'text/csv')}
    response = requests.post(f'{api_url}cria-animais-com-csv/', files=arquivo_requisicao)

print(response.status_code)
print(response.text)
