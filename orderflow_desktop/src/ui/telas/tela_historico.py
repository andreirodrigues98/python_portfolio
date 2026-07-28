import customtkinter as ctk
from dudoce_impressao_py.src.ui.tema import Tema
from datetime import datetime


class TelaHistorico(ctk.CTkFrame):

    MESES = {
        "01": "Janeiro",
        "02": "Fevereiro",
        "03": "Março",
        "04": "Abril",
        "05": "Maio",
        "06": "Junho",
        "07": "Julho",
        "08": "Agosto",
        "09": "Setembro",
        "10": "Outubro",
        "11": "Novembro",
        "12": "Dezembro"
    }
    
    def __init__(self, master, callback_reimprimir):

        super().__init__(master=master, fg_color="transparent")

        self.__callback_reimprimir = callback_reimprimir
        self.__pedidos = []

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._criar_componentes()

    def _criar_componentes(self):

        titulo = ctk.CTkLabel(master=self, text="Histórico", text_color=Tema.C1, font=ctk.CTkFont(size=28, weight="bold"))
        titulo.grid(row=0, column=0, padx=30, pady=(25, 10), sticky="w")


        self.__area_historico = ctk.CTkScrollableFrame(master=self, fg_color=Tema.C1, corner_radius=12, border_width=1, border_color=Tema.BORDA)

        self.__area_historico.grid(row=1, column=0, sticky="nsew")
        self.__area_historico.grid_columnconfigure(0, weight=1)

        self.__mensagem_vazia = ctk.CTkLabel(master=self.__area_historico, text="Nenhum pedido encontrado em histórico" ,text_color=Tema.C2)
        self.__mensagem_vazia.grid(row=0, column=0, padx=30, pady=30, sticky="e")

    def _agrupar_pedidos(self, pedidos):

        historico = {}

        for pedido in pedidos:

            if not pedido.data_pedido:
                continue 

            try:
                data_validada = datetime.strptime(
                    pedido.data_pedido,
                    "%d/%m/%Y"
                )

            except (TypeError, ValueError):

                continue

            dia = data_validada.strftime("%d")
            mes = data_validada.strftime("%m")
            ano = data_validada.strftime("%Y")

            if ano not in historico:
                historico[ano] = {}
            
            if mes not in historico[ano]:
                historico[ano][mes] = {}
            
            data_completa = f"{dia}/{mes}/{ano}"

            if data_completa not in historico[ano][mes]:
                historico[ano][mes][data_completa] = []

            historico[ano][mes][data_completa].append(pedido)
        
        return historico

    def atualizar_pedidos(self, pedidos):

        self.__pedidos = pedidos

        for componente in self.__area_historico.winfo_children():
            componente.destroy()

        historico = self._agrupar_pedidos(self.__pedidos)

        if not historico:

            mensagem = ctk.CTkLabel(master=self.__area_historico, text="Nenhum pedido encontrado no histórico.", text_color=Tema.C2)

            mensagem.grid(row=0,  column=0, padx=30, pady=30, sticky="w")

            return

        linha_ano = 0

        for ano in sorted(historico.keys(), reverse=True):

            conteudo_ano = self._criar_accordion( master=self.__area_historico, texto=ano, linha=linha_ano, nivel="ano" )

            linha_ano += 1

            meses = historico[ano]

            linha_mes = 0

            for numero_mes in sorted(
                meses.keys(),
                reverse=True
            ):

                nome_mes = self.MESES.get( numero_mes, numero_mes)

                conteudo_mes = self._criar_accordion(master=conteudo_ano, texto=nome_mes, linha=linha_mes, nivel="mes")

                linha_mes += 1

                dias = meses[numero_mes]

                linha_dia = 0

                for data_pedido in sorted(dias.keys(), key=self._converter_data_ordenacao, reverse=True):

                    pedidos_do_dia = dias[data_pedido]

                    pedidos_ordenados = sorted(pedidos_do_dia, key=lambda pedido: pedido.horario,reverse=True)

                    quantidade_pedidos = len(pedidos_ordenados)

                    if quantidade_pedidos == 1:
                        texto_qtd = f"{quantidade_pedidos} pedido"
                    else:
                        texto_qtd = f"{quantidade_pedidos} pedidos"
                    

                    texto_dia = (
                        f"{data_pedido} "
                        f"({texto_qtd})"
                    )

                    conteudo_dia = self._criar_accordion(master=conteudo_mes, texto=texto_dia, linha=linha_dia, nivel="dia")

                    linha_dia += 1

                    for indice, pedido in enumerate(pedidos_ordenados):
                        self._criar_linha_pedido(master=conteudo_dia, pedido=pedido, linha=indice)

    @staticmethod
    def _formatar_moeda(valor):

        try:
            valor = float(valor)

        except (TypeError, ValueError):
            valor = 0

        valor_formatado = (f"{valor:,.2f}".replace(",", "TEMP").replace(".", ",").replace("TEMP", "."))

        return f"R$ {valor_formatado}"

    def _criar_linha_pedido(self, master, pedido, linha):

        frame_pedido = ctk.CTkFrame(master=master, fg_color=Tema.C2, corner_radius=8, border_width=1, border_color=Tema.BORDA)
        frame_pedido.grid(row=linha, column=0, sticky="ew", padx=20, pady=5)
        frame_pedido.grid_columnconfigure(0, weight=1)

        frame_cabecalho = ctk.CTkFrame(master=frame_pedido,  fg_color="transparent" )
        frame_cabecalho.grid(row=0, column=0,  sticky="ew")
        frame_cabecalho.grid_columnconfigure(0, weight=1)

        valor_formatado = self._formatar_moeda(pedido.total)

        texto_pedido = (
            f"Pedido #{pedido.numero}  "
            f"— {pedido.horario}  "
            f"— R$ {valor_formatado}"
        )

        label_pedido = ctk.CTkLabel( master=frame_cabecalho, text=texto_pedido, text_color=Tema.TEXTO_ESCURO, anchor="w")
        label_pedido.grid(row=0, column=0, sticky="ew", padx=15,  pady=12 )

        frame_detalhes = ctk.CTkFrame(master=frame_pedido, fg_color="transparent" )
        frame_detalhes.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 15) )
        frame_detalhes.grid_remove()

        botao_expandir = ctk.CTkButton(master=frame_cabecalho,  text="▼", fg_color=Tema.C1, hover_color=Tema.BOTAO_HOVER,  width=40)
        botao_expandir.grid(row=0, column=1, padx=5,  pady=8 )

        botao_reimprimir = ctk.CTkButton(master=frame_cabecalho, text="Imprimir Cópia", width=110, fg_color=Tema.C1, hover_color=Tema.BOTAO_HOVER, text_color=Tema.TEXTO_CLARO,  command=lambda pedido_selecionado=pedido: (self.__callback_reimprimir(pedido_selecionado)))
        botao_reimprimir.grid(row=0, column=2,  padx=15, pady=8)

        if pedido.itens:
            texto_itens = "\n\n".join(pedido.itens)
        else:
            texto_itens = "Nenhum item informado."

        detalhes = (
            f"Cliente: {pedido.nome_cliente or 'Não informado'}\n"
            f"WhatsApp: {pedido.whatsapp or 'Não informado'}\n\n"
            f"Itens:\n{texto_itens}\n\n"
            f"Observação: {pedido.observacao or 'Nenhuma observação.'}\n"
            f"Impresso originalmente em: "
            f"{pedido.impresso_em or 'Ainda não impresso na tela Pedidos'}\n"
            f"Reimpressões operacionais: {pedido.texto_reimpressao}\n"
            f"Cópias pelo histórico: {pedido.quantidade_copias_historico}\n"
            f"Última cópia do histórico: "
            f"{pedido.ultima_copia_historico or 'Nenhuma'}"
        )

        label_detalhes = ctk.CTkLabel(master=frame_detalhes, text=detalhes, text_color=Tema.TEXTO_ESCURO, justify="left",  anchor="w",  wraplength=900)
        label_detalhes.grid(row=0, column=0, sticky="ew")

        def alternar_detalhes():

            if frame_detalhes.winfo_ismapped():
                frame_detalhes.grid_remove()

                botao_expandir.configure(text="▼", fg_color=Tema.C1, hover_color=Tema.BOTAO_HOVER)

            else:

                frame_detalhes.grid()
                botao_expandir.configure(text="▲", fg_color=Tema.C1, hover_color=Tema.BOTAO_HOVER)

        botao_expandir.configure(command=alternar_detalhes)

    def atualizar_pedido_reimpresso(self, pedido_atualizado):

        for indice, pedido_da_lista in enumerate(self.__pedidos):

            if pedido_da_lista.documento_id == pedido_atualizado.documento_id:

                self.__pedidos[indice] = pedido_atualizado
                break
        
        self.atualizar_pedidos(self.__pedidos)

    def _converter_data_ordenacao(self, data_texto):

        try:
            return datetime.strptime(data_texto, "%d/%m/%Y")

        except (TypeError, ValueError):

            return datetime.min

    def _criar_accordion( self, master, texto, linha, nivel):

        configuracoes = {
            "ano": {
                "fg_color": Tema.C2,
                "text_color": Tema.C1,
                "font_size": 24,
                "padx": 20
            },
            "mes": {
                "fg_color": Tema.C3,
                "text_color": Tema.C1,
                "font_size": 21,
                "padx": 20
            },
            "dia": {
                "fg_color": Tema.FUNDO_CARD,
                "text_color": Tema.C1,
                "font_size": 18,
                "padx": 20
            }
        }

        estilo = configuracoes[nivel]

        frame_accordion = ctk.CTkFrame(master=master, fg_color="transparent")

        frame_accordion.grid(row=linha, column=0, sticky="ew", padx=estilo["padx"], pady=5)

        frame_accordion.grid_columnconfigure(0, weight=1)

        botao_cabecalho = ctk.CTkButton(master=frame_accordion, text=f"▶  {texto}", anchor="w", height=45, fg_color=estilo["fg_color"], hover_color=Tema.C3, text_color=estilo["text_color"], font=ctk.CTkFont(size=estilo["font_size"], weight="bold"))

        botao_cabecalho.grid(row=0, column=0, sticky="ew")

        frame_conteudo = ctk.CTkFrame(master=frame_accordion, fg_color="transparent")
        frame_conteudo.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        frame_conteudo.grid_columnconfigure(0, weight=1)
        frame_conteudo.grid_remove()

        def alternar_accordion():

            esta_aberto = (frame_conteudo.winfo_manager() == "grid" )

            if esta_aberto:

                frame_conteudo.grid_remove()
                botao_cabecalho.configure(text=f"▶  {texto}")

            else:

                frame_conteudo.grid()
                botao_cabecalho.configure(text=f"▼  {texto}")

        botao_cabecalho.configure(command=alternar_accordion)

        return frame_conteudo
    



