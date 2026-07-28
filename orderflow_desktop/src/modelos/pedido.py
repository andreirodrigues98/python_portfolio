from datetime import datetime
from zoneinfo import ZoneInfo

class Pedido:

    def __init__(self, numero, horario, itens, total, observacao, impresso_em=None, ultima_reimpressao=None, quantidade_reimpressoes=0, 
                 documento_id= None, codigo_pedido=None, data_pedido=None, nome_cliente=None, whatsapp=None, status_impresso="nao_impresso",
                 ultima_copia_historico=None, quantidade_copias_historico=0, itens_dados=None):

        self.__numero = numero
        self.__horario = horario
        self.__itens = itens
        self.__itens_dados = itens_dados or []
        self.__total = total
        self.__observacao = observacao

        self.__impresso_em = impresso_em
        self.__ultima_reimpressao = ultima_reimpressao
        self.__quantidade_reimpressoes = quantidade_reimpressoes

        self.__documento_id = documento_id
        self.__codigo_pedido = codigo_pedido

        self.__data_pedido = data_pedido

        self.__nome_cliente = nome_cliente
        self.__whatsapp = whatsapp

        self.__status_impresso = status_impresso
        self.__ultima_copia_historico = ultima_copia_historico
        self.__quantidade_copias_historico = quantidade_copias_historico

    @property
    def numero(self):
        return self.__numero

    @property
    def nome(self):
        return self.__nome_cliente

    @property
    def horario(self):
        return self.__horario
    
    @property
    def itens(self):
        return self.__itens
    
    @property
    def itens_dados(self):
        return self.__itens_dados

    @property
    def total(self):
        return self.__total
    
    @property
    def observacao(self):
        return self.__observacao
    
    @property
    def impresso_em(self):
        return self.__impresso_em
    
    @property 
    def ultima_reimpressao(self):
        return self.__ultima_reimpressao

    @property
    def quantidade_reimpressoes(self):
        return self.__quantidade_reimpressoes

    @property
    def texto_reimpressao(self):
        if self.quantidade_reimpressoes >= 2:
            return f"{self.quantidade_reimpressoes} reimpressões"
        elif self.quantidade_reimpressoes == 1:
            return f"{self.quantidade_reimpressoes} reimpressão"
        else:
            return "Nenhuma reimpressão"

    @property
    def foi_impresso(self):

        return (self.__status_impresso == "impresso" or self.__impresso_em is not None )
    
    @property
    def documento_id(self):
        return self.__documento_id

    @property
    def status_impresso(self):
        return self.__status_impresso

    @property
    def codigo_pedido(self):
        return self.__codigo_pedido
    
    @property
    def data_pedido(self):
        return self.__data_pedido

    @property
    def nome_cliente(self):
        return self.__nome_cliente
    
    @property 
    def whatsapp(self):
        return self.__whatsapp

    @property
    def ultima_copia_historico(self):
        return self.__ultima_copia_historico

    @property
    def quantidade_copias_historico(self):
        return self.__quantidade_copias_historico

    @staticmethod
    def _formatar_itens(itens_firebase):

        if not isinstance(itens_firebase,list):
            return []

        itens_formatados = []

        for item in itens_firebase:

            if not isinstance(item, dict):
                continue

            quantidade = item.get("quantidade", 0)

            nome = str(item.get("nome", "Produto sem nome") or "Produto sem nome").strip()

            opcoes = str(item.get("opcoesTexto", "") or "" ).strip()

            try:
                quantidade = int(quantidade)

            except (TypeError, ValueError):
                quantidade = 0

            texto_item = (f"{quantidade}x {nome}" )

            if opcoes:

                opcoes = opcoes.replace(" · ", " • ")

                lista_opcoes = opcoes.split(" • ")

                for opcao in lista_opcoes:

                    opcao = opcao.strip()

                    if opcao:
                        texto_item += (f"\n• {opcao}")

            itens_formatados.append(texto_item)

        return itens_formatados

    @staticmethod
    def _formatar_data_hora(valor):

        if valor is None:
            return None

        if isinstance(valor, datetime):

            valor_brasilia = valor.astimezone(ZoneInfo("America/Sao_Paulo"))

            return valor_brasilia.strftime("%d/%m/%Y %H:%M")

        return str(valor)

    @classmethod
    def from_dict(cls, dados):

        if not isinstance(dados, dict ):

            raise TypeError("Os dados do pedido devem ser um dicionário." )

        cliente = dados.get("cliente" )

        if not isinstance(cliente,  dict):

            cliente = {}

        valores = dados.get("valores")

        if not isinstance(valores, dict):

            valores = {}

        impressao = dados.get("impressao" )

        if not isinstance(impressao, dict):
            impressao = {}

        historico_dados = dados.get("historico" )

        if not isinstance(historico_dados, dict):
            historico_dados = {}

        itens_dados = dados.get("itens")

        if not isinstance(itens_dados, list):

            itens_dados = []

        itens_formatados = cls._formatar_itens(itens_dados)

        data_criacao = dados.get("createdAt")

        data_pedido = ""
        horario_pedido = ""

        if isinstance(data_criacao, datetime ):

            data_criacao = data_criacao.astimezone(ZoneInfo("America/Sao_Paulo"))
            data_pedido = data_criacao.strftime("%d/%m/%Y")
            horario_pedido = data_criacao.strftime("%H:%M")

        total_estimado = valores.get("totalEstimado",  0)

        try:
            total_estimado = float(total_estimado )

        except (TypeError, ValueError):
            total_estimado = 0

        quantidade_impressoes = impressao.get("quantidadeImpressoes", 0)

        try:
            quantidade_impressoes = int(quantidade_impressoes)

        except (TypeError, ValueError):
            quantidade_impressoes = 0

        quantidade_impressoes = max(quantidade_impressoes, 0)

        quantidade_reimpressoes = max(
            quantidade_impressoes - 1, 0)

        quantidade_copias_historico = (
            historico_dados.get("quantidadeCopias", 0))

        try:
            quantidade_copias_historico = int(quantidade_copias_historico)

        except (TypeError, ValueError):
            quantidade_copias_historico = 0

        quantidade_copias_historico = max(quantidade_copias_historico,0)

        status_impresso = impressao.get("status", "nao_impresso")

        if status_impresso not in ("impresso", "nao_impresso"):

            status_impresso = ("nao_impresso")

        impresso_em = cls._formatar_data_hora(impressao.get("impressoEm"))

        ultima_reimpressao = (cls._formatar_data_hora(impressao.get("ultimaImpressaoEm")))
        ultima_copia_historico = (cls._formatar_data_hora(historico_dados.get("ultimaCopiaEm")))

        pedido = cls(
            numero=dados.get("numeroPedidoFormatado", ""),
            horario=horario_pedido,
            itens=itens_formatados,
            total=total_estimado,
            observacao=dados.get("observacoes", ""),
            impresso_em=impresso_em,
            ultima_reimpressao=(ultima_reimpressao),
            quantidade_reimpressoes=(quantidade_reimpressoes),
            documento_id=dados.get("documento_id"),
            codigo_pedido=dados.get("codigoPedido"),
            data_pedido=data_pedido,
            nome_cliente=cliente.get( "nome", ""),
            whatsapp=cliente.get("whatsapp", ""),
            status_impresso=status_impresso,
            ultima_copia_historico=(ultima_copia_historico),
            quantidade_copias_historico=(quantidade_copias_historico),
            itens_dados=itens_dados
        )

        return pedido

    def marcar_impresso(self):

        agora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M")

        self.__impresso_em = agora
        self.__ultima_reimpressao = agora
        self.__status_impresso = "impresso"

    def registrar_reimpressao(self):

        agora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M")

        self.__quantidade_reimpressoes += 1
        self.__ultima_reimpressao = agora
        self.__status_impresso = "impresso"

    def to_dict(self):
        
        pedido_dict = {
            "numero": self.numero,
            "horario": self.horario,
            "nome": self.nome,
            "itens": self.itens,
            "total": self.total,
            "observacao": self.observacao,
            "impresso_em": self.impresso_em,
            "ultima_reimpressao": self.ultima_reimpressao,
            "quantidade_reimpressoes": self.quantidade_reimpressoes
        }

        return pedido_dict
  
    def registrar_copia_historico(self):

        agora = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M")

        self.__quantidade_copias_historico += 1
        self.__ultima_copia_historico = agora