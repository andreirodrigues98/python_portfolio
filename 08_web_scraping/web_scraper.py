from openpyxl import Workbook
from openpyxl.styles import Font
import requests
from bs4 import BeautifulSoup

CONST_URL = ['https://books.toscrape.com/', 'https://books.toscrape.com/catalogue/page-2.html']

def baixar_pagina(url):
    try:
        resposta = requests.get(url, timeout=10)
        resposta.raise_for_status()
        return resposta.text

    except requests.RequestException as erro:
        print(f"Erro ao acessar {url}: {erro}")
        return None

def interpretar_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    return soup

def localizar_produtos(soup):
    lista = soup.find_all("article", class_="product_pod")
    dados = []



    for produto in lista:
        h3 = produto.find("h3")
        a = h3.find("a")
        nome = a.get('title')


        div_product_price = produto.find("div", class_='product_price')
        p = div_product_price.find("p", class_="price_color")
        preco = float(p.get_text(strip=True).replace("Â", "").replace("£", ""))


        p_estoque = div_product_price.find("p", class_="instock availability")
        estoque = p_estoque.get_text(strip=True)


        produtos = {
            "nome": nome,
            "preco": preco,
            "estoque": estoque
        }

        dados.append(produtos)
    
    return dados

def exportar_txt(dados):

    maior_preco = dados[0]['preco']
    menor_preco = dados[0]['preco']
    produto_maior = dados[0]['nome']
    produto_menor = dados[0]['nome']
    qtd_total = 0
    lista_txt = []

    for produto in dados:
        nome = produto['nome']
        preco = produto['preco']
        estoque = produto['estoque']

        qtd_total += 1

        if preco > maior_preco:
            maior_preco = preco
            produto_maior = nome
        
        if preco < menor_preco:
            menor_preco = preco
            produto_menor = nome
        
        product = {
            "nome": nome,
            "preco": preco,
            "estoque": estoque
        }

        lista_txt.append(product)
    
        
    relatorio_txt = {
        "quantidade": qtd_total,
        "maior_valor": maior_preco,
        "menor_valor": menor_preco,
        "produto_maior": produto_maior,
        "produto_menor": produto_menor
    }

    with open("relatorio_webscraper.txt", "w", encoding="utf-8") as arquivo:
        
        arquivo.write("========== RESUMO DOS LIVROS ==========\n")
        arquivo.write(f"Quantidade de Livros: {relatorio_txt['quantidade']}\n\n")

        arquivo.write(f"Livro mais caro: {relatorio_txt['produto_maior']}\n")
        arquivo.write(f"Valor: £ {relatorio_txt['maior_valor']:.2f}\n\n")

        arquivo.write(f"Livro mais barato: {relatorio_txt['produto_menor']}\n")
        arquivo.write(f"Valor: £ {relatorio_txt['menor_valor']:.2f}\n\n")

        arquivo.write("========== RELATÓRIO DOS LIVROS ==========\n")
        
        for livro in lista_txt:
            arquivo.write(f"Livro: {livro['nome']}\n")
            arquivo.write(f"Preço: £ {livro['preco']:.2f}\n")
            arquivo.write(f"Estoque: {livro['estoque']}\n\n")
        
    print("\nRelatorio em .txt criado com sucesso!")

    return lista_txt

def exportar_excel(lista_txt):
     
    wb = Workbook()

    aba = wb.active
    aba.title = 'Livros'

    aba.append(['Nome', 'Preço', 'Estoque'])

    aba.column_dimensions["A"].width = 70
    aba.column_dimensions["B"].width = 15
    aba.column_dimensions["C"].width = 20

    aba.freeze_panes = "A2"

    for col in aba[1]:
        col.font = Font(bold=True)

    for book in lista_txt:
        aba.append([book['nome'], book['preco'], book['estoque']])

    wb.save("relatorio_webscraper.xlsx")

    print("Planilha criada com sucesso!")

def main():

    todos_produtos = []

    for link in CONST_URL:
        html = baixar_pagina(link)

        if not html:
            continue 

        soup = interpretar_html(html)
        dados = localizar_produtos(soup)
        
        if not dados:
            print("Nenhum dado disponível para exportação.")
            return []

        todos_produtos.extend(dados)
    
    if not todos_produtos:
        print("Nenhum produto foi encontrado.")
        return

    lista_txt = exportar_txt(todos_produtos)
    exportar_excel(lista_txt)

if __name__ == '__main__':
    main()