import os
import sys

from pathlib import Path


NOME_APLICACAO = "Dudoce"


def esta_compilado():

    return bool(
        getattr(
            sys,
            "frozen",
            False
        )
    )


def obter_pasta_raiz():

    if esta_compilado():

        return (
            Path(sys.executable)
            .resolve()
            .parent
        )

    return (
        Path(__file__)
        .resolve()
        .parents[3]
    )


def obter_pasta_dados():

    if esta_compilado():

        local_appdata = os.getenv(
            "LOCALAPPDATA"
        )

        if local_appdata:

            pasta_dados = (
                Path(local_appdata)
                / NOME_APLICACAO
            )

        else:

            pasta_dados = (
                Path.home()
                / NOME_APLICACAO
            )

    else:

        pasta_dados = (
            obter_pasta_raiz()
        )

    pasta_dados.mkdir(
        parents=True,
        exist_ok=True
    )

    return pasta_dados


def obter_caminho_configuracao():

    pasta_configuracoes = (
        obter_pasta_dados()
        / "configuracoes"
    )

    pasta_configuracoes.mkdir(
        parents=True,
        exist_ok=True
    )

    return (
        pasta_configuracoes
        / "config.json"
    )


def obter_caminho_credencial():

    return (
        obter_pasta_raiz()
        / "credenciais"
        / "dudoce.json"
    )


def obter_caminho_recurso(
    *partes
):

    if (
        esta_compilado()
        and hasattr(
            sys,
            "_MEIPASS"
        )
    ):

        pasta_base = Path(
            sys._MEIPASS
        )

    else:

        pasta_base = (
            obter_pasta_raiz()
        )

    return pasta_base.joinpath(
        "recursos",
        *partes
    )