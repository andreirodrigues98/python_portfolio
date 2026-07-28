from pathlib import Path 
import csv 



def converter_csv_txt():

    caminho = input('Digite o caminho do arquivo csv: ').strip()

    if not caminho:
        print('Preencha o campo corretamente!')
        return 
    
    caminho = Path(caminho)

    if not caminho.exists():
        print('Arquivo inexistente!')
        return 
    
    if not caminho.is_file():
        print('Esse caminho não pertence a um arquivo!')
        return 
    
    if caminho.suffix.lower() != '.csv':
        print('O arquivo não é csv')
        return 
    
    caminho_txt = input('Digite o nome do arquivo txt que será criado: ').strip()

    if not caminho_txt:
        print('Preencha o campo corretamente!')
        return 
    
    if not caminho_txt.lower().endswith('.txt'):
        caminho_txt += '.txt'

    caminho_txt = Path(caminho_txt)

    with open(caminho, 'r', encoding='utf-8', newline='') as arquivo:
        leitor = csv.reader(arquivo)

        with open(caminho_txt, 'w', encoding='utf-8') as arquivo_txt:
            for linha in leitor:
                linha_formatada = ' | '.join(linha)
                arquivo_txt.write(linha_formatada + '\n')

    print('Arquivo convertido com sucesso!')


if __name__ == '__main__':
    converter_csv_txt()

    
    