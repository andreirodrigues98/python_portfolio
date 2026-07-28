# 📚 Projeto 08 — Web Scraper de Livros

Aplicação desenvolvida em Python para coletar dados de livros disponíveis em um site de testes para web scraping.

O programa acessa diferentes páginas, extrai informações dos produtos, analisa os preços e gera relatórios nos formatos TXT e Excel.

---

## 🚀 Funcionalidades

- Acesso automático às páginas do site
- Extração do nome dos livros
- Extração do preço
- Extração da disponibilidade em estoque
- Coleta de dados de múltiplas páginas
- Identificação do livro mais caro
- Identificação do livro mais barato
- Contagem da quantidade de livros encontrados
- Geração de relatório em TXT
- Geração de planilha Excel
- Formatação automática da planilha

---

## 🌐 Site utilizado

O projeto utiliza o site:

```text
Books to Scrape
```

O site foi criado especificamente para estudos e práticas de web scraping.

---

## 🛠 Tecnologias utilizadas

- Python 3
- Requests
- BeautifulSoup
- OpenPyXL

---

## 📁 Estrutura do projeto

```text
08_web_scraper_livros/
├── web_scraper.py
├── requirements.txt
├── README.md
├── .gitignore
└── exemplos/
    ├── relatorio_webscraper.txt
    └── relatorio_webscraper.xlsx
```

---

## ⚙️ Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/python-portfolio.git
```

Entre na pasta do projeto:

```bash
cd python-portfolio/08_web_scraper_livros
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como executar

Execute o arquivo principal:

```bash
python web_scraper.py
```

Após a execução, serão criados os arquivos:

```text
relatorio_webscraper.txt
relatorio_webscraper.xlsx
```

---

## 📊 Dados coletados

Para cada livro, o programa coleta:

- Nome
- Preço
- Disponibilidade em estoque

Exemplo:

```text
Livro: A Light in the Attic
Preço: £ 51.77
Estoque: In stock
```

---

## 📄 Relatório TXT

O arquivo `relatorio_webscraper.txt` apresenta:

- quantidade de livros encontrados;
- livro mais caro;
- preço do livro mais caro;
- livro mais barato;
- preço do livro mais barato;
- relação completa dos livros coletados.

---

## 📗 Relatório Excel

O arquivo `relatorio_webscraper.xlsx` possui as colunas:

| Nome | Preço | Estoque |
|------|------:|---------|
| Livro coletado | £ 00.00 | In stock |

A planilha também conta com:

- cabeçalho em negrito;
- largura personalizada das colunas;
- primeira linha congelada;
- dados organizados em formato tabular.

---

## 📚 Conceitos praticados

- Web scraping
- Requisições HTTP
- Interpretação de HTML
- BeautifulSoup
- Seletores HTML
- Listas
- Dicionários
- Funções
- Estruturas de repetição
- Manipulação de arquivos TXT
- Manipulação de planilhas Excel
- Análise e agrupamento de dados
- Tratamento de respostas HTTP

---

## 🔮 Melhorias futuras

- Automatizar a paginação
- Permitir que o usuário escolha a quantidade de páginas
- Adicionar tratamento completo de erros de conexão
- Exportar os dados para CSV e JSON
- Criar gráficos com os preços coletados
- Aplicar filtros na planilha
- Salvar a URL de cada livro
- Coletar a avaliação em estrelas
- Criar uma interface com Streamlit
- Armazenar os dados em um banco SQLite

---

## ⚠️ Uso responsável

Web scraping deve ser realizado respeitando as regras, os termos de uso e as limitações de cada site.

Este projeto utiliza um ambiente criado especificamente para práticas educacionais.

---

## 👨‍💻 Autor
Desenvolvido por Andrei Rodrigues
Projeto desenvolvido como parte do meu portfólio de estudos em Python.
