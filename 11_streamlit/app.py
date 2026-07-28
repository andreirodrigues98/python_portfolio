import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon="📊",
    layout="wide"
)

vendas = [
    {"produto": "Mouse", "categoria": "Informática", "valor": 500.0},
    {"produto": "Teclado", "categoria": "Informática", "valor": 600.0},
    {"produto": "Caderno", "categoria": "Papelaria", "valor": 300.0},
    {"produto": "Caneta", "categoria": "Papelaria", "valor": 125.0},
    {"produto": "Monitor", "categoria": "Informática", "valor": 2400.0}
]

def calcular_total(vendas):

    soma_total = 0

    for venda in vendas:
        valor = venda["valor"]

        soma_total += valor
    
    return soma_total

def calcular_qtd(vendas):
    qtd_vendido = len(vendas)

    return qtd_vendido

def calcular_media(soma_total, qtd_vendido):

    if qtd_vendido == 0:
       return 0

    media = soma_total / qtd_vendido
    
    return media

def categorias(vendas):
    categorias = ["Geral"]

    for venda in vendas:
        categoria = venda["categoria"]

        if categoria not in categorias:
            categorias.append(categoria)
    
    return categorias

def filtrar_vendas(vendas, categoria_escolhida):
    
    if categoria_escolhida == "Geral":
        return vendas
    
    vendas_filtradas = []

    for venda in vendas:
        if venda["categoria"] == categoria_escolhida:
            vendas_filtradas.append(venda)
    
    return vendas_filtradas

def resumo_categoria(vendas):
    resumo = {}

    for venda in vendas:

        categoria = venda["categoria"]
        valor = venda["valor"]

        if categoria not in resumo:
            resumo[categoria] = 0
        
        resumo[categoria] += valor
    
    return resumo

def resumo_categoria_lista(resumo):
    lista_resumo = []

    for categoria, valor in resumo.items():
        
        item = {
            "categoria": categoria,
            "valor": valor
        }

        lista_resumo.append(item)

    
    return lista_resumo


opcoes = categorias(vendas)

st.sidebar.title("Filtros")
st.sidebar.write("Use as opções abaixo para analisar as vendas.")
categoria_escolhida = st.sidebar.selectbox("Escolha uma categoria:", opcoes)

vendas_filtradas = filtrar_vendas(vendas, categoria_escolhida)
soma_total = calcular_total(vendas_filtradas)
qtd_vendido = calcular_qtd(vendas_filtradas)
media = calcular_media(soma_total, qtd_vendido)
resumo = resumo_categoria(vendas)
lista_resumo = resumo_categoria_lista(resumo)

st.title("Dashboard Vendas")
st.write("Esse Dashboard nos trará um resumo de como foram as vendas neste mês.")

st.subheader("Indicadores:")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Total Vendido", value=f" R$ {soma_total:,.2f}")

with col2:
    st.metric(label="Qtd de Vendas", value=qtd_vendido)

with col3:
    st.metric(label="Média de Vendas", value=f"{media:,.2f}")

st.subheader("Vendas Filtradas:")

dados_filtrados = pd.DataFrame(vendas_filtradas)
st.dataframe(dados_filtrados, use_container_width=True)

st.subheader("Vendas por Categoria: ")
df_grafico = pd.DataFrame(lista_resumo)
st.bar_chart(df_grafico, x="categoria", y="valor")
