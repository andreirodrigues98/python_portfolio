import firebase_admin 
from firebase_admin import credentials
from firebase_admin import firestore
from dudoce_impressao_py.src.modelos.pedido import Pedido

class FirebaseService:
    
    def __init__(self, caminho_credencial, nome_colecao):

        self.__caminho_credencial = caminho_credencial
        self.__nome_colecao = nome_colecao

        self.__cliente = None

        self._inicializar_firebase()
    
    def _inicializar_firebase(self):

        try:
            firebase_admin.get_app()

        except ValueError:
            credencial = credentials.Certificate(
                self.__caminho_credencial
            )

            firebase_admin.initialize_app(credencial)

        self.__cliente = firestore.client()

    def buscar_pedidos(self):

        pedidos = []

        documentos = (self.__cliente.collection(self.__nome_colecao).stream())

        for documento in documentos:
            try:
                pedido = (self._converter_documento_em_pedido(documento))
                pedidos.append(pedido)

            except Exception as erro:
                print( "Documento ignorado durante ""a busca de pedidos:", documento.id,repr(erro))

        return pedidos

    def _converter_documento_em_pedido(self, documento):

        if documento is None:
            raise ValueError("Documento do Firebase não informado.")

        dados = documento.to_dict()

        if not isinstance(dados, dict):
            raise ValueError("Documento do Firebase inválido.")

        dados_pedido = dict(dados)

        dados_pedido["documento_id"] = documento.id

        return Pedido.from_dict(dados_pedido)
        
    def escutar_pedidos(self, callback_alteracao, callback_erro=None):

        colecao = (self.__cliente.collection(self.__nome_colecao ))

        primeira_leitura = True

        def ao_receber_snapshot(documentos, mudancas, horario_leitura):

            nonlocal primeira_leitura

            for mudanca in mudancas:
                try:
                    tipo_alteracao = ( mudanca.type.name)
                    pedido = ( self._converter_documento_em_pedido(mudanca.document))

                    callback_alteracao(tipo_alteracao, pedido, primeira_leitura)

                except Exception as erro:
                    if callback_erro is not None:
                        callback_erro(erro)

                    else:
                        print("Erro no listener do Firebase:",repr(erro))

            primeira_leitura = False

        observador = colecao.on_snapshot(ao_receber_snapshot)

        return observador
    
    def marcar_pedido_como_impresso(self, documento_id):

        if not documento_id:
            raise ValueError("O pedido não possui documento_id.")

        referencia = (self.__cliente.collection(self.__nome_colecao).document(documento_id))

        referencia.update({
            "impressao.status": "impresso",
            "impressao.impressoEm": firestore.SERVER_TIMESTAMP,
            "impressao.ultimaImpressaoEm": firestore.SERVER_TIMESTAMP,
            "impressao.quantidadeImpressoes": 1
        })

    def registrar_reimpressao(self, documento_id):
        if not documento_id:
            raise ValueError("O pedido não possui documento_id.")

        referencia = (self.__cliente.collection(self.__nome_colecao).document(documento_id))

        referencia.update({
            "impressao.status": "impresso",
            "impressao.ultimaImpressaoEm": firestore.SERVER_TIMESTAMP,
            "impressao.quantidadeImpressoes": firestore.Increment(1)
        })    

    def registrar_copia_historico(self, documento_id):

        if not documento_id:
            raise ValueError("O pedido não possui documento_id.")

        referencia = (self.__cliente .collection(self.__nome_colecao).document(documento_id) )
        referencia.update({"historico.ultimaCopiaEm": firestore.SERVER_TIMESTAMP,"historico.quantidadeCopias": firestore.Increment(1)})
