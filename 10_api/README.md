# 🚀 Projeto 10 — API de Livros com FastAPI

API REST desenvolvida em Python para coletar informações de livros por meio de web scraping e disponibilizar os dados em endpoints HTTP.

A aplicação permite listar livros, pesquisar títulos e comparar o preço atual com um valor desejado pelo usuário.

---

## 📌 Funcionalidades

- Coleta de livros por web scraping
- Extração do nome dos livros
- Extração do preço
- Extração da disponibilidade em estoque
- Coleta de dados de múltiplas páginas
- Listagem de todos os livros pela API
- Busca parcial pelo nome do livro
- Comparação com um preço desejado
- Cálculo da diferença entre os preços
- Retorno de erro HTTP 404 para livros não encontrados
- Documentação automática com Swagger

---

## 🌐 Site utilizado

O projeto utiliza o site:

```text
Books to Scrape
```

O site foi criado especificamente para estudos e práticas de web scraping.

---

## 🛠 Tecnologias utilizadas

- Python 3.10 ou superior
- FastAPI
- Uvicorn
- Requests
- BeautifulSoup

---

## 📁 Estrutura do projeto

```text
10_api_livros_fastapi/
├── api.py
├── scraper.py
├── requirements.txt
├── README.md
├── .gitignore
└── exemplos/
    ├── lista_livros.json
    └── comparacao_preco.json
```

---

## ⚙️ Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/python-portfolio.git
```

Entre na pasta do projeto:

```bash
cd python-portfolio/10_api_livros_fastapi
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

Inicie o servidor com:

```bash
uvicorn api:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

---

## 📖 Documentação interativa

O FastAPI gera automaticamente uma documentação interativa.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

## 🔗 Endpoints

### Listar todos os livros

```http
GET /livros
```

Exemplo:

```text
http://127.0.0.1:8000/livros
```

Exemplo de resposta:

```json
[
    {
        "nome": "A Light in the Attic",
        "preco": 51.77,
        "estoque": "In stock"
    }
]
```

---

### Buscar um livro pelo nome

```http
GET /livros/{nome}
```

Exemplo:

```text
http://127.0.0.1:8000/livros/A Light in the Attic
```

Não é necessário informar obrigatoriamente o título completo, pois a busca considera parte do nome.

Exemplo de resposta:

```json
{
    "nome": "A Light in the Attic",
    "preco": 51.77,
    "estoque": "In stock"
}
```

---

### Comparar com um preço desejado

Utilize o parâmetro de consulta:

```text
preco_desejado
```

Exemplo:

```text
http://127.0.0.1:8000/livros/A Light in the Attic?preco_desejado=40
```

Quando o livro ainda estiver acima do valor desejado:

```json
{
    "livro": "A Light in the Attic",
    "preco": 51.77,
    "preco_desejado": 40.0,
    "diferenca": 11.77,
    "compre_agora": "Aguarde até que chegue ao valor desejado"
}
```

Quando o livro estiver dentro do valor desejado:

```json
{
    "livro": "A Light in the Attic",
    "preco": 51.77,
    "preco_desejado": 60.0,
    "compre_agora": "O preço está conforme o esperado, compre já!"
}
```

---

## ❌ Livro não encontrado

Quando nenhum livro correspondente for localizado, a API retorna:

```text
HTTP 404 Not Found
```

Exemplo de resposta:

```json
{
    "detail": "livro não encontrado"
}
```

---

## 📚 Conceitos praticados

- Desenvolvimento de API REST
- FastAPI
- Criação de endpoints
- Parâmetros de rota
- Query parameters
- Respostas JSON
- Códigos de status HTTP
- Tratamento de erro HTTP 404
- Web scraping
- Requests
- BeautifulSoup
- Interpretação de HTML
- Listas
- Dicionários
- Funções
- Separação de responsabilidades
- Organização em módulos

---

## ⚠️ Limitações atuais

- Os dados são coletados novamente a cada requisição
- A versão atual consulta apenas duas páginas
- A API depende da disponibilidade do site externo
- A busca retorna o primeiro livro correspondente
- Ainda não existe armazenamento em banco de dados

---

## 🔮 Melhorias futuras

- Adicionar tratamento completo de erros de conexão
- Implementar cache para evitar scraping em todas as requisições
- Automatizar a paginação
- Criar modelos de resposta com Pydantic
- Validar o preço desejado
- Adicionar filtros por preço e estoque
- Adicionar ordenação dos resultados
- Criar paginação da API
- Armazenar os livros em SQLite
- Criar testes automatizados com Pytest
- Utilizar Docker
- Publicar a API em um serviço de hospedagem

---

## ⚠️ Uso responsável

Web scraping deve ser realizado respeitando os termos de uso, políticas e limitações de cada site.

Este projeto utiliza um ambiente criado especificamente para práticas educacionais.

---

## 👨‍💻 Autor

Projeto desenvolvido como parte do meu portfólio de estudos em Python.
