from planilha import carregar_cadastros, validar_cadastro, salvar_resultados
from automacao import abrir_site, fazer_login, preencher_formulario

def main():

    URL = "https://andreirodrigues98.github.io/12_automacao_site_planilha_python_portfolio/"
    EMAIL_LOGIN = "teste@gmail.com" 
    SENHA_LOGIN = "123456"

    caminho_arquivo = "cadastros_teste_automacao.xlsx"

    cadastros = carregar_cadastros(caminho_arquivo)

    validos = []
    invalidos = []
    resultados = []

    for cadastro in cadastros:

        valido, mensagem = validar_cadastro(cadastro)

        if valido:
            validos.append(cadastro)
        else:
            copia_cadastro = cadastro.copy()
            copia_cadastro["erro"] = mensagem

            invalidos.append(copia_cadastro)

    abrir_site(URL)
    fazer_login(EMAIL_LOGIN, SENHA_LOGIN)

    for cadastro in validos:

        try:
            preenchido = preencher_formulario(cadastro)

            if preenchido:
                resultado = {
                "nome": cadastro["nome"],
                "status": "Sucesso",
                "mensagem": "Cadastro realizado"
                }   

                resultados.append(resultado)
            else:
                resultado = {
                    "nome": cadastro["nome"],
                    "status": "Erro",
                    "mensagem": "A automação não confirmou o cadastro"
                }

                resultados.append(resultado)

        except Exception as erro:
            resultado = {
            "nome": cadastro.get("nome", ""),
            "status": "Erro",
            "mensagem": str(erro)
            }
            resultados.append(resultado)

    salvar_resultados(resultados, invalidos, "relatorio_automacao.xlsx")

if __name__ == "__main__":
    main()