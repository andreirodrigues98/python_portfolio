import winsound

from dudoce_impressao_py.src.dudoce.caminhos import (obter_caminho_recurso)

class SomService:
    
    def __init__(self):
        
        self.__som_service = True

        self.__caminho = (obter_caminho_recurso("sons", "novo_pedido.wav"))
        
    @property
    def ativado(self):
        return self.__som_service

    def tocar_novo_pedido(self):

        if not self.__som_service:
            return 

        self._reproduzir_som()

    def tocar_teste(self):

        self._reproduzir_som()

    def _reproduzir_som(self):

        if self.__caminho.exists():

            winsound.PlaySound(
                str(self.__caminho),
                winsound.SND_FILENAME
                | winsound.SND_ASYNC
            )

        else:

            winsound.MessageBeep(
                winsound.MB_ICONEXCLAMATION
            )

    def ativar(self):

        self.__som_service = True
    
    def desativar(self):
        
        self.__som_service =  False

    def definir_ativado(self, ativado):

        self.__som_service = bool(ativado)