import customtkinter as ctk
from dudoce_impressao_py.src.ui.tema import Tema 

class CardResumo(ctk.CTkFrame):

    def __init__(self, master, titulo, valor="0"):

        super().__init__(master=master, fg_color=Tema.C1, corner_radius=10, border_width=1, border_color=Tema.BORDA)

        self.grid_columnconfigure(0, weight=1)

        label_titulo = ctk.CTkLabel(master=self, text=titulo, text_color=Tema.C2, font=ctk.CTkFont(size=20, weight="bold"))
        label_titulo.grid(row=0, column=0, padx=15, pady=(15, 5))

        self.__label_valor = ctk.CTkLabel(master=self, text=valor, text_color=Tema.C2, font=ctk.CTkFont(size=16, weight="bold"))
        self.__label_valor.grid(row=1, column=0, padx=15, pady=(0, 15))
 
    def atualizar_valor(self, valor):
        
        self.__label_valor.configure(text=valor)






