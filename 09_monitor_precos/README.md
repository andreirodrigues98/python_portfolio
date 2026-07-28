# 💷 Projeto 09 — Verificador de Preços de Livros

Aplicação desenvolvida em Python para consultar preços de livros em um site de testes de web scraping, comparar o valor atual com um preço desejado e registrar o resultado das consultas em um arquivo JSON.

---

## 🚀 Funcionalidades

- Coleta de dados de livros por web scraping
- Extração do nome, preço e disponibilidade
- Busca parcial pelo título do livro
- Definição de um preço desejado pelo usuário
- Comparação entre preço atual e preço desejado
- Cálculo da diferença entre os valores
- Registro da data e hora da consulta
- Armazenamento permanente do histórico em JSON
- Tratamento de arquivo JSON vazio ou inválido

---

## 🔍 Como funciona

O programa realiza as seguintes etapas:

1. Acessa o site utilizado no projeto
2. Coleta os livros disponíveis na página
3. Solicita o nome do livro
4. Solicita o preço desejado
5. Compara o preço atual com o valor informado
6. Exibe o resultado no terminal
7. Registra a consulta no histórico

---

## 🌐 Site utilizado

O projeto utiliza o site:

```text
Books to Scrape
```

Esse site foi desenvolvido especificamente para estudos e práticas de web scraping.

---

## 🛠 Tecnologias utilizadas

- Python 3
- Requests
- BeautifulSoup
- JSON
- pathlib
- datetime

---

## 📁 Estrutura do projeto

```text
09_verificador_precos_livros/
├── monitor_precos.py
├── requirements.txt
├── README.md
├── .gitignore
└── exemplos/
    └── historico_precos_exemplo.json
```

---

## ⚙️ Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/python-portfolio.git
```

Entre na pasta do projeto:

```bash
cd python-portfolio/09_verificador_precos_livros
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## ▶️ Como executar

Execute o arquivo principal:

```bash
python monitor_precos.py
```

O programa solicitará:

```text
Informe o nome do livro que deseja buscar:
Informe o preço que você deseja:
```

---

## 💷 Comparação de preços

Quando o valor atual estiver dentro do preço desejado, o programa exibirá um alerta:

```text
ALERTA: O LIVRO JÁ ESTÁ DENTRO DO PREÇO DESEJADO!
```

Caso o preço ainda esteja acima do esperado, serão apresentados:

- preço atual;
- preço desejado;
- diferença entre os valores.

Os valores são exibidos em libra esterlina porque essa é a moeda utilizada pelo site analisado.

---

## 📄 Histórico das consultas

As consultas são armazenadas no arquivo:

```text
historico_precos.json
```

Cada registro contém:

```json
{
    "produto": "Nome do livro",
    "preco_atual": 25.50,
    "preco_desejado": 20.00,
    "atingiu_preco": false,
    "data_consulta": "10/08/2026 15:30"
}
```

O histórico é mantido mesmo após o encerramento do programa.

---

## 📚 Conceitos praticados

- Web scraping
- Requisições HTTP
- BeautifulSoup
- Interpretação de HTML
- Listas
- Dicionários
- Funções
- Busca parcial
- Comparação de valores
- Manipulação de JSON
- Persistência de dados
- pathlib
- datetime
- Validação de entradas
- Tratamento de exceções

---

## ⚠️ Limitação atual

A versão atual realiza a verificação apenas quando o programa é executado.

Ela ainda não executa consultas automaticamente em intervalos periódicos nem envia notificações externas.

---

## 🔮 Melhorias futuras

- Automatizar a consulta em horários definidos
- Enviar alerta por e-mail
- Enviar notificação pelo Telegram
- Consultar várias páginas
- Exibir vários resultados encontrados
- Criar um menu interativo
- Permitir visualizar o histórico
- Salvar o link de cada livro
- Criar gráficos com o histórico dos preços
- Utilizar banco de dados SQLite
- Criar uma interface com Streamlit

---

## ⚠️ Uso responsável

Web scraping deve ser realizado respeitando os termos de uso, as limitações e as políticas de cada site.

Este projeto utiliza um ambiente desenvolvido para práticas educacionais.

---

## 👨‍💻 Autor
Desenvolvido por Andrei Rodrigues
Projeto desenvolvido como parte do meu portfólio de estudos em Python.
