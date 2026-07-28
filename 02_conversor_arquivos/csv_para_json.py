from pathlib import Path 
import json 
import csv 


def converter_csv_json():
    caminho = input('Digite o caminho do arquivo csv: ').strip()

    if not caminho: 
        print('Preencha o campo corretamente!')
        return 
    
    csv_arquivo = Path(caminho)

    if not csv_arquivo.exists():
        print('Arquivo inexistente!')
        return 
    
    if not csv_arquivo.is_file():
        print('Esse caminho não pertence a um arquivo!')
        return 
    
    if csv_arquivo.suffix.lower() != '.csv':
        print('O arquivo não é csv')
        return 
    
    caminho_json = input('Digite o nome do arquivo json que será criado: ').strip()

    if not caminho_json: 
        print('Preencha o campo corretamente!')
        return 
    
    if not caminho_json.endswith('.json'):
        caminho_json += '.json'
    
    json_arquivo = Path(caminho_json)

    dados = []

    with open(csv_arquivo, 'r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            dados.append(linha)
        
        with open(json_arquivo, 'w', encoding='utf-8') as arquivo_json:
            json.dump(dados, arquivo_json, ensure_ascii=False, indent=4)
    
    print('Arquivo convertido com sucesso')




if __name__ == '__main__':
    converter_csv_json()

