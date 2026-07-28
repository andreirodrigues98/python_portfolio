# 📊 Projeto 11 — Dashboard de Vendas com Streamlit

Dashboard interativo desenvolvido em Python para visualizar e analisar dados de vendas.

A aplicação apresenta indicadores financeiros, filtro por categoria, tabela com os registros e gráfico com o total vendido por categoria.

---

## 🚀 Funcionalidades

- Visualização do total vendido
- Visualização da quantidade de vendas
- Cálculo da média por venda
- Filtro interativo por categoria
- Atualização dos indicadores conforme o filtro
- Exibição dos dados em uma tabela
- Agrupamento das vendas por categoria
- Geração de gráfico de barras
- Interface acessível pelo navegador

---

## 📊 Indicadores apresentados

O dashboard apresenta:

- Total vendido
- Quantidade de vendas
- Média por venda
- Valores vendidos por categoria

---

## 🛠 Tecnologias utilizadas

- Python 3
- Streamlit
- Pandas

---

## 📁 Estrutura do projeto

```text
11_dashboard_streamlit/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── imagens/
    ├── dashboard_geral.png
    └── dashboard_filtrado.png
```

---

## ⚙️ Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/python-portfolio.git
```

Entre na pasta do projeto:

```bash
cd python-portfolio/11_dashboard_streamlit
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como executar

Execute o seguinte comando:

```bash
streamlit run app.py
```

Após a inicialização, a aplicação será aberta no navegador.

---

## 🔎 Filtro por categoria

Na barra lateral, o usuário pode selecionar uma categoria.

As opções disponíveis são geradas automaticamente com base nos dados cadastrados.

Exemplo:

```text
Geral
Informática
Papelaria
```

Quando uma categoria é selecionada, os indicadores e a tabela são atualizados.

---

## 📈 Indicadores

O dashboard possui três indicadores principais:

### Total vendido

Apresenta a soma de todas as vendas consideradas pelo filtro.

### Quantidade de vendas

Apresenta a quantidade de registros encontrados.

### Média por venda

Apresenta o valor médio das vendas selecionadas.

---

## 📋 Tabela de vendas

Os dados filtrados são convertidos em um DataFrame do Pandas e exibidos em uma tabela.

As colunas apresentadas são:

| Produto | Categoria | Valor |
|---------|-----------|------:|
| Mouse | Informática | R$ 500,00 |
| Teclado | Informática | R$ 600,00 |

---

## 📊 Gráfico de vendas

O dashboard apresenta um gráfico de barras com o valor vendido por categoria.

Essa visualização permite comparar rapidamente o desempenho das categorias cadastradas.

---

## 📸 Demonstração

Adicione nesta seção imagens do projeto.

### Visão geral

```markdown
![Dashboard geral](imagens/dashboard_geral.png)
```

### Dashboard filtrado

```markdown
![Dashboard filtrado](imagens/dashboard_filtrado.png)
```

---

## 📚 Conceitos praticados

- Desenvolvimento de aplicações com Streamlit
- Criação de dashboards
- Pandas
- DataFrames
- Listas
- Dicionários
- Funções
- Filtros
- Agregação de dados
- Cálculo de indicadores
- Interface interativa
- Visualização de dados
- Organização de código

---

## ⚠️ Limitações atuais

- Os dados estão cadastrados diretamente no código
- Ainda não existe integração com arquivo CSV ou Excel
- Não existe banco de dados
- O dashboard possui apenas um gráfico
- As vendas não podem ser cadastradas pela interface

---

## 🔮 Melhorias futuras

- Importar vendas de um arquivo CSV
- Importar dados de uma planilha Excel
- Permitir o upload de arquivos pela interface
- Adicionar filtro por produto
- Adicionar filtro por faixa de preço
- Adicionar filtro por período
- Criar novos gráficos
- Permitir cadastrar vendas pela aplicação
- Exportar os dados filtrados
- Conectar a um banco de dados SQLite
- Publicar o dashboard online
- Criar autenticação de usuário

---

## 👨‍💻 Autor
Desenvolvido por Andrei Rodrigues
Projeto desenvolvido como parte do meu portfólio de estudos em Python.
