from pathlib import Path  
import json

ARQUIVO = Path('produtos.json')

def carregar_produtos():

    if not ARQUIVO.exists():
        print('Nenhum arquivo encontrado!')
        return []
    
    with open(ARQUIVO, 'r', encoding='utf-8') as arquivo_json:
        produtos = json.load(arquivo_json)

    return produtos

def cadastrar_produto(produtos):
    
    nome = input('\nInforme o nome do produto: ').strip()

    if not nome:
        print('Preencha o campo corretamente!')
        return 
        
    while True:

        try:
            preco = float(input(f'Informe o preço do produto {nome}: ').strip())

            if preco <= 0:
                print('Preço deve ser maior que 0')
                continue 
            else:
                break
        except ValueError:
            print('Informe um valor válido.')
            continue 

    while True:
        try:
            qtd = int(input(f'Informe a quantidade do produto {nome}: ').strip())

            if qtd < 0:
                print('A quantidade deve ser maior ou igual a 0')
                continue 
            else:
                break
        except ValueError:
            print('Informe uma quantidade inteira válida.')
            continue 
        
    categoria = input(f'Informe a categoria do produto {nome}: ').strip()

    if not categoria:
        print('Preencha o campo corretamente.')
        return
        
    valor_estoque = qtd * preco

    dic_produto = {
            "nome": nome,
            "preco": preco,
            "quantidade": qtd,
            "categoria": categoria,
            "valor": valor_estoque
        }

    produtos.append(dic_produto)

    print('Produto Cadastrado com sucesso!')
    salvar_json(produtos) 

def listar_produtos(produtos):

    if not produtos:
        print('Nenhum produto na cadastrado!')
        return 
    
    for indice,produto in enumerate(produtos, start=1):
        print(f'\nProduto {indice}: ')
        print(f"Nome: {produto['nome']}\nPreço: R$ {produto['preco']:.2f}\nQuantidade: {produto['quantidade']}\nCategoria: {produto['categoria']}\nValor em estoque: R$ {produto['valor']:.2f}")

def buscar_produto(produtos):

    if not produtos:
        print('Nenhum produto cadastrado!')
        return 
    
    nome_produto = input('Informe o nome do produto que deseja buscar: ').strip().lower()

    if not nome_produto:
        print('Preencha o campo corretamente!')
        return 
    
    resultados = []
    
    for produto in produtos:
        if nome_produto in produto['nome'].lower():
            resultados.append(produto)
    
    if not resultados:
        print('Nenhum produto encontrado!')
        return 
        
    elif len(resultados) == 1:
        print('\n1 Produto Encontrado.')
        encontrado = resultados[0]
        print(f"Nome: {encontrado['nome']}\nPreço: R$ {encontrado['preco']:.2f}\nQuantidade: {encontrado['quantidade']}\nCategoria: {encontrado['categoria']}\nValor em estoque: R$ {encontrado['valor']:.2f}")
        return encontrado

    else:
        print(f'\n{len(resultados)} Produtos Encontrados')

        for indice, produto in enumerate(resultados, start=1):
            print(f'\nProduto {indice}: ')
            print(f"Nome: {produto['nome']}\nPreço: R$ {produto['preco']:.2f}\nQuantidade: {produto['quantidade']}\nCategoria: {produto['categoria']}\nValor em estoque: R$ {produto['valor']:.2f}")
            
        
        escolha = escolha_produto(resultados)
        escolhido = resultados[escolha - 1]
        
        print(f'\nProduto Escolhido!')
        print(f"\nNome: {escolhido['nome']}\nPreço: R$ {escolhido['preco']:.2f}\nQuantidade: {escolhido['quantidade']}\nCategoria: {escolhido['categoria']}\nValor em estoque: R$ {escolhido['valor']:.2f}")
    return escolhido

def valor_total_estoque(produtos):

    if not produtos:
        print('Nenhum produto cadastrado!')
        return

    total = 0

    for produto in produtos:
        total += produto['valor']

    print(f'\nValor total em estoque: R$ {total:.2f}')

def atualizar_estoque(produtos):

    if not produtos:
        print('Nenhum produto cadastrado!')
        return 
    
    produto = buscar_produto(produtos)

    if not produto:
        print('Nenhum produto encontrado!')
        return 

    while True:

        try: 
            qtd = int(input('Informe a quantidade nova de estoque: ').strip())

            if qtd < 0:
                print('A quantidade deve ser maior ou igual a 0.')
                continue 

            else:
                produto['quantidade'] = qtd
                produto['valor'] = produto['quantidade'] * produto['preco']
                salvar_json(produtos)
                print('Quantidade alterada com sucesso!')
                break
        except ValueError:
            print('Informe uma quantidade valida.')
            continue 

def escolha_produto(resultados):

    while True:

        try:
            escolha = int(input('\nInforme o numero do produto escolhido: '))

            if escolha < 1 or escolha > len(resultados):
                print('Informe uma opção valida.')
                continue 

            else:
                return escolha 
        except ValueError:
            print('Digite um numero válido!')
            continue 

def salvar_json(produtos):
    with open(ARQUIVO, 'w', encoding='utf-8') as arquivo_json:
        json.dump(produtos, arquivo_json, ensure_ascii=False, indent=4)

    print('Produtos salvos no json com sucesso!')

def verificar_opcao():

    while True:

        try:
            opcao = int(input('Informe a opção desejada: ').strip())

            if opcao < 0 or opcao > 5:
                print('Digite uma opção valida!')
                continue 

            else:
                return opcao

        except ValueError:
            print('Informe uma opção valida!')
            continue 

def menu():
    
    print('\n========== MENU ==========')
    print('1 - Cadastrar Produtos')
    print('2 - Listar Produtos')
    print('3 - Buscar Produtos')
    print('4 - Atualizar Estoque')
    print('5 - Ver Valor Total do Estoque')
    print('0 - Sair')

def main():

    produtos = carregar_produtos()

    while True:
        menu()

        opcao = verificar_opcao()
    
        if opcao == 1:
            while True:
                cadastrar_produto(produtos)

                continuar = input('Deseja continuar cadastrando [s/n]? ').strip().lower()

                if continuar in ['s', 'sim']:
                    continue

                elif continuar in ['nao', 'n', 'não']:
                    break

                else:
                    print('Opção não reconhecida, voltando ao menu...')
                    break
        
        elif opcao == 2:
            listar_produtos(produtos)

        elif opcao == 3:
            buscar_produto(produtos)

        elif opcao == 4:
            atualizar_estoque(produtos)
        
        elif opcao == 5:
            valor_total_estoque(produtos)

        elif opcao == 0:
            print('Finalizando o sistema...')
            break 

if __name__ == '__main__':
    main()