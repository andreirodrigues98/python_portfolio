from dudoce_impressao_py.src.modelos.pedido import Pedido

class GerenciadorPedidos:

    def __init__(self):

        self.__pedidos_nao_impressos = []
        self.__pedidos_impressos = []

    def _pedido_ja_existe(self, pedido):

        todos_pedidos = ( self.__pedidos_nao_impressos + self.__pedidos_impressos )

        if pedido.documento_id:

            return any(pedido_existente.documento_id == pedido.documento_id for pedido_existente in todos_pedidos)

        return pedido in todos_pedidos

    def adicionar_pedido(self, pedido):

        if self._pedido_ja_existe(pedido):

            return False

        if pedido.foi_impresso:
            self.__pedidos_impressos.append(pedido)

        else:
            self.__pedidos_nao_impressos.append(pedido)

        return True

    def imprimir_pedido(self, pedido):
        
        pedido.marcar_impresso()

        if pedido in self.__pedidos_nao_impressos:
            self.__pedidos_nao_impressos.remove(pedido)

        if pedido not in self.__pedidos_impressos:
            self.__pedidos_impressos.append(pedido)

    def reimprimir_pedido(self, pedido):
        
        pedido.registrar_reimpressao()

    def listar_nao_impressos(self):
        return self.__pedidos_nao_impressos

    def listar_impressos(self):
        return self.__pedidos_impressos

    def quantidade_nao_impressos(self):
        return len(self.__pedidos_nao_impressos)
    
    def quantidade_impressos(self):
        return len(self.__pedidos_impressos)
    
    def atualizar_pedido(self, pedido_atualizado):

        self.remover_pedido(pedido_atualizado.documento_id)

        self.adicionar_pedido(pedido_atualizado)

    def remover_pedido(self, documento_id):

        self.__pedidos_nao_impressos = [pedido for pedido in self.__pedidos_nao_impressos if pedido.documento_id != documento_id]

        self.__pedidos_impressos = [pedido for pedido in self.__pedidos_impressos if pedido.documento_id != documento_id]
