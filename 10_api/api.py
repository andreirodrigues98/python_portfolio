from fastapi import FastAPI, HTTPException
from scraper import obter_livros

app = FastAPI()

# uvicorn api:app --reload

@app.get("/livros")
def listar_livros():
    return obter_livros()

@app.get("/livros/{nome}")
def preco_livros_diferenca(nome: str, preco_desejado: float | None = None):
    livros = obter_livros()

    for livro in livros:
        if nome.lower() in livro["nome"].lower():

            if preco_desejado is None:
                return livro
           
            if livro["preco"] <= preco_desejado:

                compre_agora = "O preço está conforme o esperado, compre já!"

                dicionario_buscado = {
                    "livro": livro['nome'],
                    "preco": livro['preco'],
                    "preco_desejado": preco_desejado,
                    "compre_agora": compre_agora
                }

                return dicionario_buscado

            else:
                diferenca = livro["preco"] - preco_desejado

                compre_agora = "Aguarde até que chegue ao valor desejado"

                dicionario_buscado = {
                    "livro": livro['nome'],
                    "preco": livro['preco'],
                    "preco_desejado": preco_desejado,
                    "diferenca": round(diferenca, 2),
                    "compre_agora": compre_agora
                }

                return dicionario_buscado
                
    raise HTTPException(status_code=404, detail="livro não encontrado")
    