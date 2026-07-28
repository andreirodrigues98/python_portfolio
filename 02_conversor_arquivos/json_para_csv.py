from pathlib import Path 
import csv 
import json 



def converter_json_csv():
    
    caminho = input('Digite o caminho do arquivo json: ').strip()

    if not caminho:
        print('Preencha o campo corretamente!')
        return
    
    arquivo_json = Path(caminho)

    if not arquivo_json.exists():
        print('O caminho não existe')
        return 
    
    if not arquivo_json.is_file():
        print('O caminho não pertence a um arquivo!')
        return 
    
    if arquivo_json.suffix.lower() != '.json':
        print('O arquivo não é json')
        return 
    
    caminho_csv = input('Digite o nome do arquivo csv que vai ser criado: ').strip()

    if not caminho_csv:
        print('Preencha o campo corretamente!')
        return 
    
    if not caminho_csv.lower().endswith('.csv'):
        caminho_csv += '.csv'
    
    arquivo_csv = Path(caminho_csv)

    with open(arquivo_json, 'r', encoding='utf-8') as arq_json:
        dados_json = json.load(arq_json)

        if not dados_json:
            print('Não há dados para converter.')
            return 
        
        cabecalho = dados_json[0].keys()

        with open(arquivo_csv, 'w', encoding='utf-8', newline='') as arq_csv:
            dados_csv = csv.DictWriter(arq_csv, fieldnames=cabecalho)
            dados_csv.writeheader()  # cabecalho (header --> html)
            dados_csv.writerows(dados_json) # linhas
            print('Arquivo convertido com sucesso!')

if __name__ == '__main__':
    converter_json_csv()
