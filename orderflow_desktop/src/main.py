import customtkinter as ctk
from dudoce_impressao_py.src.dudoce.interface import AplicacaoDudoce

def iniciar_aplicacao():

    ctk.set_appearance_mode("light")
    app = AplicacaoDudoce(titulo="Dudôce - Pedidos", largura=1200, altura=700)
    app.mainloop()

if __name__ == "__main__":
    iniciar_aplicacao()