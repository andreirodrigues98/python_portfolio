import requests
from bs4 import BeautifulSoup

URLS = ['https://books.toscrape.com/', 'https://books.toscrape.com/catalogue/page-2.html']

def baixar_pagina(link):
    
    url = link

    resposta = requests.get(url)

    if resposta.status_code == 200:
        html = resposta.text
        return html
    else:
        print(f"Não foi possivel verificar a URL, Erro {resposta.status_code}!")
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

def obter_livros():

    todos_produtos = []

    for link in URLS:
        html = baixar_pagina(link)

        if not html:
            continue

        soup = interpretar_html(html)
        dados = localizar_produtos(soup)

        todos_produtos.extend(dados)
    
    return todos_produtos

def main():
    livros = obter_livros()

if __name__ == '__main__':
    main()