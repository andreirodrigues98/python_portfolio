import matplotlib.pyplot as plt

vendas = [
    {"produto": "Mouse", "categoria": "Informática", "valor": 500.0},
    {"produto": "Teclado", "categoria": "Informática", "valor": 600.0},
    {"produto": "Caderno", "categoria": "Papelaria", "valor": 300.0},
    {"produto": "Caneta", "categoria": "Papelaria", "valor": 125.0},
    {"produto": "Monitor", "categoria": "Informática", "valor": 2400.0}
]

def resumo_categorias(vendas):

    if not vendas:
        print("A lista esta vazia!")
        return 
    
    total_vendido = 0
    maior_valor = vendas[0]['valor']
    menor_valor = vendas[0]['valor']
    produto_maior_venda = vendas[0]['produto']
    produto_menor_venda = vendas[0]['produto']
    categorias = {}

    for venda in vendas:
        categoria = venda['categoria']
        valor = venda['valor']

        total_vendido += valor

        if valor > maior_valor:
            maior_valor = valor
            produto_maior_venda = venda['produto']
        
        if valor < menor_valor:
            menor_valor = valor
            produto_menor_venda = venda['produto']
        
        if categoria not in categorias:
            categorias[categoria] = 0 
        
        categorias[categoria] += valor

    print("\n========== DASHBOARD ==========")
    print(f"Total Vendido: R$ {total_vendido:.2f}")
    print(f"Quantidade de vendas: {len(vendas)}")
    print(f"Maior venda: {produto_maior_venda} no valor de R$ {maior_valor:.2f}")
    print(f"Menor venda: {produto_menor_venda} no valor de R$ {menor_valor:.2f}")

    for categoria, valor in categorias.items():
        print(f"{categoria}: R$ {valor:.2f}")

    quantidade = len(vendas)
    soma = total_vendido
    media = soma / quantidade


    dados = {
        "quantidade": quantidade,
        "total": soma,
        "media": media,
        "maior_valor": maior_valor,
        "menor_valor": menor_valor,
        "produto_maior_venda": produto_maior_venda,
        "produto_menor_venda": produto_menor_venda
    }

    return dados, categorias

def gerar_relatorio_txt(dados):

    with open("relatorio_vendas.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write("========== Relatório Dashboard ==========\n")
        arquivo.write(f"Quantidade de vendas: {dados['quantidade']}\n")
        arquivo.write(f"Total Vendido: R$ {dados['total']:.2f}\n")
        arquivo.write(f"Média por venda: R$ {dados['media']:.2f}\n\n")

        arquivo.write(f"Produto com maior venda: {dados['produto_maior_venda']}\n")
        arquivo.write(f"Maior Valor: R$ {dados['maior_valor']:.2f}\n\n")

        arquivo.write(f"Produto com menor venda: {dados['produto_menor_venda']}\n")
        arquivo.write(f"Menor Valor: R$ {dados['menor_valor']:.2f}\n\n")

    print("\nRelatorio em .txt criado com sucesso!")

def gerar_dashboard(categorias):
    nomes_categorias = []
    valores_vendidos = []

    for nome in categorias:
        nomes_categorias.append(nome)
        valores_vendidos.append(categorias[nome])
    
    plt.bar(nomes_categorias, valores_vendidos) 
    plt.title("Vendas por Categoria") 
    plt.xlabel("Categoria") 
    plt.ylabel("Total vendido em R$") 

    plt.savefig("dashboard.png")

    plt.close()

    print("Grafico foi salvo como imagem com sucesso!")

def main():
    resultado = resumo_categorias(vendas)

    if not resultado:
        return 

    dados, categorias = resultado
    
    gerar_relatorio_txt(dados)
    gerar_dashboard(categorias)
    

if __name__ == '__main__':
    main()