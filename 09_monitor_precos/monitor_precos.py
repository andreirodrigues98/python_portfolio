import json
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup

CONST_URL = 'https://books.toscrape.com/'
ARQUIVO_HISTORICO = Path("historico_precos.json")

def baixar_pagina():
    try:
        resposta = requests.get(CONST_URL, timeout=10)
        resposta.raise_for_status()
        return resposta.text

    except requests.RequestException as erro:
        print(f"Erro ao acessar o site: {erro}")
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

def buscar_produto(dados):

    while True:
        nome_livro = input("Informe o nome do livro que deseja buscar: ").strip().lower()

        if not nome_livro:
            print("Preencha o campo corretamente!")
            continue 

        encontrado = False

        for livro in dados:
            if nome_livro in livro['nome'].lower():
                book = livro
                encontrado = True
                break
        
        if not encontrado:
            print("Não existe nenhum livro com este nome em sistema!")
            print("Tente novamente")
            continue 

        return book

def solicitar_preco_desejado():

    while True:
        try:
            preco_desejado = float(input("Informe o preco que vc deseja: ").strip())

            if preco_desejado <= 0:
                print("Preencha com um valor válido")
                continue 
            
            return preco_desejado

        except ValueError:
            print("Preencha com um valor válido")
            continue 
    
def comparar_preco(book, preco_desejado):
    
    if book['preco'] <= preco_desejado:
        print("\n\nALERTA: O LIVRO JÁ ESTÁ DENTRO DO PREÇO DESEJADO!")
        print(f"\nLivro: {book['nome']}\nPreço Atual: £ {book['preco']:.2f}\nPreço Desejado: £ {preco_desejado:.2f}")
        return True
    
    else:
        diferenca = book['preco'] - preco_desejado
        print("\n\nO LIVRO AINDA NÃO CHEGOU NO PREÇO DESEJADO!")
        print(f"Livro: {book['nome']}\nPreço Atual: £ {book['preco']:.2f}\nPreço Desejado: £ {preco_desejado:.2f}\nDiferença: £ {diferenca:.2f}")
        return False
    
def carregar_historico():

    if not ARQUIVO_HISTORICO.exists():
        return []

    if ARQUIVO_HISTORICO.stat().st_size == 0:
        return []

    try:
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as arquivo:
            historico = json.load(arquivo)

        if not isinstance(historico, list):
            return []

        return historico

    except json.JSONDecodeError:
        return []

def salvar_historico(historico):
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as arquivo:
        json.dump(historico, arquivo, ensure_ascii=False, indent=4)

def registrar_consulta(book, preco_desejado, atingiu_preco):
    historico = carregar_historico()

    data_consulta = datetime.now().strftime("%d/%m/%Y %H:%M")

    registro = {
        "produto": book["nome"],
        "preco_atual": book["preco"],
        "preco_desejado": preco_desejado,
        "atingiu_preco": atingiu_preco,
        "data_consulta": data_consulta
    }

    historico.append(registro)
    salvar_historico(historico)
    print("\nConsulta registrada no histórico!\n")

def main():

    html = baixar_pagina()

    if not html:
        return 
    
    soup = interpretar_html(html)
    dados = localizar_produtos(soup) 

    if not dados:
        return 
    
    book = buscar_produto(dados)
    preco_desejado = solicitar_preco_desejado()
    atingiu_preco = comparar_preco(book, preco_desejado)
    registrar_consulta(book, preco_desejado, atingiu_preco)

if __name__ == '__main__':
    main()