import customtkinter as ctk
from dudoce_impressao_py.src.ui.tema import Tema

class CardRelatorio(ctk.CTkFrame):

    def __init__(self, master, pedido, linha):

        super().__init__(master=master, fg_color=Tema.C1, corner_radius=10, border_width=1, border_color=Tema.BORDA)

        self.__pedido = pedido
        self.__detalhes_abertos = False

        self.grid(row=linha, column=0, sticky="ew", padx=20, pady=8)
        self.grid_columnconfigure(0, weight=1)

        self._criar_cabecalho()
        self._criar_detalhes()

    @staticmethod
    def _formatar_moeda(valor):

        try:
            valor = float(valor)

        except (TypeError, ValueError):
            valor = 0

        valor_formatado = (f"{valor:,.2f}".replace(",", "TEMP").replace(".", ",").replace("TEMP", "."))

        return f"R$ {valor_formatado}"

    def _criar_cabecalho(self):

        frame_cabecalho = ctk.CTkFrame( master=self,  fg_color="transparent")

        frame_cabecalho.grid(row=0,  column=0, padx=15, pady=12, sticky="ew")

        frame_cabecalho.grid_columnconfigure(0, weight=1)
        frame_cabecalho.grid_columnconfigure(1, weight=1)
        frame_cabecalho.grid_columnconfigure(2, weight=1)
        frame_cabecalho.grid_columnconfigure(3, weight=1)
        frame_cabecalho.grid_columnconfigure(4, weight=0)

        

        numero_pedido = (self.__pedido.numero or "Não informado")
        nome_cliente = (self.__pedido.nome_cliente or "Cliente não informado" )
        data_pedido = (self.__pedido.data_pedido  or "Data não informada")
        horario_pedido = (self.__pedido.horario or "Horário não informado")
        texto_pedido = (f"Pedido #{numero_pedido}")

        label_pedido = ctk.CTkLabel( master=frame_cabecalho, text=texto_pedido, text_color=Tema.C2, font=ctk.CTkFont(size=15, weight="bold"),anchor="w")
        label_pedido.grid(row=0, column=0, sticky="w", padx=(0, 10))

        label_cliente = ctk.CTkLabel(master=frame_cabecalho, text=nome_cliente, text_color=Tema.C2, font=ctk.CTkFont( size=14 ), anchor="w")

        label_cliente.grid(row=0, column=1, sticky="w", padx=10)

        texto_data_horario = ( f"{data_pedido} "f"às {horario_pedido}")
        label_data_horario = ctk.CTkLabel( master=frame_cabecalho, text=texto_data_horario,  text_color=Tema.C2,  font=ctk.CTkFont(size=14))
        label_data_horario.grid( row=0, column=2,  padx=10 )

        texto_total = self._formatar_moeda( self.__pedido.total)
        label_total = ctk.CTkLabel(master=frame_cabecalho, text=texto_total, text_color=Tema.C2,  font=ctk.CTkFont(size=15,  weight="bold"))

        label_total.grid(row=0, column=3, padx=10 )

        self.__botao_detalhes = ctk.CTkButton(master=frame_cabecalho, text="Ver detalhes",width=120, text_color=Tema.C1,  
        fg_color=Tema.C2, hover_color=Tema.C3, command=self._alternar_detalhes)

        self.__botao_detalhes.grid(row=0, column=4, padx=(10, 0))

    def _criar_detalhes(self):

        self.__frame_detalhes = ctk.CTkFrame(master=self, fg_color="transparent")
        self.__frame_detalhes.grid_columnconfigure(0, weight=1)

        nome_cliente = (self.__pedido.nome_cliente or "Cliente não informado")
        whatsapp = (self.__pedido.whatsapp  or "Não informado")

        texto_cliente = (f"Cliente: {nome_cliente}\n" f"WhatsApp: {whatsapp}")

        label_cliente = ctk.CTkLabel(master=self.__frame_detalhes, text=texto_cliente, text_color=Tema.C2, justify="left", anchor="w", font=ctk.CTkFont(size=14))

        label_cliente.grid(row=0, column=0, sticky="ew", padx=20, pady=(5, 10))

        texto_itens = "\n\n".join(self.__pedido.itens)

        if not texto_itens:
            texto_itens = "Nenhum item informado."

        label_itens = ctk.CTkLabel(master=self.__frame_detalhes,text=("Itens do pedido:\n\n"f"{texto_itens}"),
            text_color=Tema.C2, justify="left", anchor="w",  wraplength=900, font=ctk.CTkFont(size=14))
        label_itens.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        observacao = (self.__pedido.observacao or "Nenhuma observação." )

        label_observacao = ctk.CTkLabel(master=self.__frame_detalhes, text=f"Observação: {observacao}",
            text_color=Tema.C2, justify="left", anchor="w",  wraplength=900, font=ctk.CTkFont(size=14))

        label_observacao.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        if self.__pedido.foi_impresso:
            data_impressao = (self.__pedido.impresso_em  or "Data não informada")
            texto_status = ("Status: Impresso\n"f"Impresso em: {data_impressao}")

        else:
            texto_status = ("Status: Não impresso")

        label_status = ctk.CTkLabel(master=self.__frame_detalhes, text=texto_status, text_color=Tema.C2,  justify="left",  anchor="w", font=ctk.CTkFont(size=14, weight="bold"))

        label_status.grid(row=3, column=0, sticky="ew", padx=20, pady=(10, 15))

    def _alternar_detalhes(self):

        if self.__detalhes_abertos:

            self.__frame_detalhes.grid_remove()

            self.__botao_detalhes.configure(
                text="Ver detalhes"
            )

            self.__detalhes_abertos = False

        else:

            self.__frame_detalhes.grid(
                row=1,
                column=0,
                sticky="ew",
                padx=15,
                pady=(0, 15)
            )

            self.__botao_detalhes.configure(
                text="Ocultar detalhes"
            )

            self.__detalhes_abertos = True


