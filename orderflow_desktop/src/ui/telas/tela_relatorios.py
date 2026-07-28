import customtkinter as ctk
from dudoce_impressao_py.src.ui.tema import Tema
from dudoce_impressao_py.src.ui.cards.card_resumo import CardResumo
from dudoce_impressao_py.src.ui.cards.card_relatorio import CardRelatorio

class TelaRelatorios(ctk.CTkFrame):
    
    def __init__(self, master, callback_gerar_relatorio):

        super().__init__(master=master, fg_color="transparent")

        self.__cards_resumo = {}
        self.__callback_gerar_relatorio = callback_gerar_relatorio

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1, minsize=380)

        self._criar_componentes()

    def _criar_componentes(self):

        titulo = ctk.CTkLabel(master=self, text="Relatórios", text_color=Tema.C1, font=ctk.CTkFont(size=28, weight="bold"))
        titulo.grid(row=0, column=0, padx=30, pady=(25, 10), sticky="w")

        frame_conteudo_superior = ctk.CTkFrame(master=self, fg_color="transparent")
        frame_conteudo_superior.grid(row=1, column=0, sticky="ew", padx=30, pady=(10, 15))
        frame_conteudo_superior.grid_columnconfigure(0, weight=1)
        
        self._criar_area_filtros(frame_conteudo_superior)
        self._criar_cards_resumo(frame_conteudo_superior)
        self._criar_area_resultados()

    def _atualizar_placeholder_periodo(self, tipo):

        placeholders = {"Diário": "DD/MM/AAAA", "Mensal": "MM/AAAA","Anual": "AAAA"}

        self.__entrada_periodo.delete( 0, "end" )

        placeholder = placeholders.get(tipo, "DD/MM/AAAA")

        self.__entrada_periodo.configure(placeholder_text=placeholder)

    def _criar_area_filtros(self, master):

        frame_filtros = ctk.CTkFrame(master=master, fg_color=Tema.C1, corner_radius=10, border_width=1, border_color=Tema.BORDA)
        frame_filtros.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        frame_filtros.grid_columnconfigure(1, weight=1)

        label_tipo = ctk.CTkLabel(master=frame_filtros, text="Tipo:", text_color=Tema.C2, font=ctk.CTkFont(size=24, weight="bold"))
        label_tipo.grid(row=0, column=0, padx=(20, 8), pady=20)

        self.__seletor_tipo = ctk.CTkOptionMenu(master=frame_filtros, values=["Diário", "Mensal", "Anual"], fg_color=Tema.C2, button_color=Tema.C3, button_hover_color=Tema.BORDA, text_color=Tema.TEXTO_ESCURO, command=self._atualizar_placeholder_periodo)
        self.__seletor_tipo.grid(row=0, column=1, padx=8, pady=20, sticky="w")

        label_periodo = ctk.CTkLabel(master=frame_filtros, text="Período:", text_color=Tema.C2, font=ctk.CTkFont(size=15, weight="bold"))
        label_periodo.grid(row=0, column=2, padx=(20, 8), pady=20)

        self.__entrada_periodo = ctk.CTkEntry(master=frame_filtros, width=160, placeholder_text="DD/MM/AAAA", fg_color=Tema.C2, text_color=Tema.TEXTO_ESCURO, border_color=Tema.BORDA)
        self.__entrada_periodo.grid(row=0, column=3, padx=8, pady=20)

        self.__botao_gerar = ctk.CTkButton(master=frame_filtros, text="Gerar Relatório", text_color=Tema.C1, fg_color=Tema.C2, hover_color=Tema.C3, command=self._gerar_relatorio)
        self.__botao_gerar.grid(row=0, column=4, padx=20, pady=20)

    def _criar_cards_resumo(self, master):

        frame_cards = ctk.CTkFrame(master=master, fg_color="transparent")

        frame_cards.grid(row=1, column=0, sticky="ew")

        frame_cards.grid_columnconfigure(0, weight=1)

        frame_cards_principais = ctk.CTkFrame(master=frame_cards, fg_color="transparent")

        frame_cards_principais.grid(row=0, column=0, sticky="ew")

        cards_principais = [
            ("pedidos", "Pedidos"),
            ("valor_total", "Valor Total"),
            ("ticket_medio", "Ticket Médio"),
            ("impressos", "Impressos"),
            ("nao_impressos", "Não Impressos")
        ]

        for coluna in range(len(cards_principais)):

            frame_cards_principais.grid_columnconfigure(coluna, weight=1)

        for coluna, configuracao in enumerate(cards_principais):

            chave, titulo = configuracao

            card = CardResumo(master=frame_cards_principais, titulo=titulo, valor="0")

            card.grid( row=0, column=coluna, sticky="nsew", padx=5)

            self.__cards_resumo[chave] = card

        frame_cards_detalhes = ctk.CTkFrame(master=frame_cards, fg_color="transparent")

        frame_cards_detalhes.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        cards_detalhes = [
            ("maior_pedido", "Maior Pedido"),
            ("menor_pedido", "Menor Pedido"),
            ("horario_pico", "Horário de Pico")
        ]

        for coluna in range(len(cards_detalhes)):

            frame_cards_detalhes.grid_columnconfigure(coluna, weight=1)

        for coluna, configuracao in enumerate(cards_detalhes):

            chave, titulo = configuracao

            card = CardResumo(master=frame_cards_detalhes, titulo=titulo, valor="-")

            card.grid(row=0, column=coluna, sticky="nsew", padx=5)

            self.__cards_resumo[chave] = card

    def _criar_area_resultados(self):

        self.__abas_resultados = ctk.CTkTabview(
            master=self,
            fg_color=Tema.C1,
            segmented_button_fg_color=Tema.C2,
            segmented_button_selected_color=Tema.C3,
            segmented_button_selected_hover_color=Tema.C3,
            segmented_button_unselected_color=Tema.C2,
            segmented_button_unselected_hover_color=Tema.C3,
            text_color=Tema.C1,
            corner_radius=10,
            border_width=0,
            height=420
        )

        self.__abas_resultados.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=30,
            pady=(0, 25)
        )

        aba_pedidos = self.__abas_resultados.add(
            "Pedidos"
        )

        aba_produtos = self.__abas_resultados.add(
            "Produtos vendidos"
        )

        aba_pedidos.grid_columnconfigure(
            0,
            weight=1
        )

        aba_pedidos.grid_rowconfigure(
            0,
            weight=1
        )

        self.__area_resultados = ctk.CTkScrollableFrame(
            master=aba_pedidos,
            fg_color=Tema.C1,
            corner_radius=0
        )

        self.__area_resultados.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.__area_resultados.grid_columnconfigure(
            0,
            weight=1
        )

        mensagem = ctk.CTkLabel(
            master=self.__area_resultados,
            text=(
                "Selecione um período "
                "e gere o relatório."
            ),
            text_color=Tema.C2
        )

        mensagem.grid(
            row=0,
            column=0,
            padx=25,
            pady=25,
            sticky="w"
        )

        aba_produtos.grid_columnconfigure(
            0,
            weight=1
        )

        aba_produtos.grid_columnconfigure(
            1,
            weight=1
        )

        aba_produtos.grid_rowconfigure(
            0,
            weight=1
        )

        frame_produtos = ctk.CTkFrame(
            master=aba_produtos,
            fg_color="transparent"
        )

        frame_produtos.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew"
        )

        frame_produtos.grid_columnconfigure(
            0,
            weight=1
        )

        frame_produtos.grid_columnconfigure(
            1,
            weight=1
        )

        frame_produtos.grid_rowconfigure(
            1,
            weight=1
        )

        titulo_produtos = ctk.CTkLabel(
            master=frame_produtos,
            text="Produtos vendidos",
            text_color=Tema.C2,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        titulo_produtos.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(15, 10)
        )

        titulo_ranking = ctk.CTkLabel(
            master=frame_produtos,
            text="Ranking dos produtos",
            text_color=Tema.C2,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        titulo_ranking.grid(
            row=0,
            column=1,
            sticky="w",
            padx=20,
            pady=(15, 10)
        )

        self.__area_produtos_vendidos = (
            ctk.CTkScrollableFrame(
                master=frame_produtos,
                fg_color=Tema.C1,
                border_width=1,
                border_color=Tema.C2
            )
        )

        self.__area_produtos_vendidos.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(15, 8),
            pady=(0, 15)
        )

        self.__area_produtos_vendidos.grid_columnconfigure(
            0,
            weight=1
        )

        self.__area_ranking_produtos = (
            ctk.CTkScrollableFrame(
                master=frame_produtos,
                fg_color=Tema.C1,
                border_width=1,
                border_color=Tema.C2
            )
        )

        self.__area_ranking_produtos.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8, 15),
            pady=(0, 15)
        )

        self.__area_ranking_produtos.grid_columnconfigure(
            0,
            weight=1
        )

    @staticmethod
    def _formatar_moeda(valor):

        try:
            valor = float(valor)

        except (TypeError, ValueError):
            valor = 0

        valor_formatado = (f"{valor:,.2f}".replace(",", "TEMP").replace(".", ",").replace("TEMP", "."))

        return f"R$ {valor_formatado}"

    def atualizar_relatorio(self, resultado):

        self.__cards_resumo[ "pedidos"].atualizar_valor(str(resultado["quantidade_pedidos"]))
        self.__cards_resumo["valor_total"].atualizar_valor(f"R$ {resultado['valor_total']:,.2f}" )
        self.__cards_resumo[ "ticket_medio"].atualizar_valor( f"R$ {resultado['ticket_medio']:,.2f}")
        self.__cards_resumo[ "impressos"].atualizar_valor(str(resultado[ "quantidade_impressos" ]))
        self.__cards_resumo["nao_impressos" ].atualizar_valor(str(resultado[ "quantidade_nao_impressos"]))

        maior_pedido = resultado.get( "maior_pedido" )
        menor_pedido = resultado.get( "menor_pedido")

        if maior_pedido is not None:

            texto_maior_pedido = (
                f"#{maior_pedido.numero}"
                f" • {maior_pedido.data_pedido}\n"
                f"R$ {maior_pedido.total:,.2f}"
            )

        else:
            texto_maior_pedido = "-"

        self.__cards_resumo[ "maior_pedido" ].atualizar_valor(texto_maior_pedido)

        if menor_pedido is not None:

            texto_menor_pedido = (
                f"#{menor_pedido.numero}"
                f" • {menor_pedido.data_pedido}\n"
                f"R$ {menor_pedido.total:,.2f}"
            )

        else:
            texto_menor_pedido = "-"

        self.__cards_resumo["menor_pedido"].atualizar_valor( texto_menor_pedido)

        horario_pico = resultado.get( "horario_mais_pedidos")
        quantidade_horario = resultado.get("quantidade_horario_mais_pedidos", 0)

        if horario_pico is not None:
            hora_inicial = int(horario_pico)
            hora_final = (hora_inicial + 1) % 24

            if quantidade_horario == 1:
                texto_qtd_horario = "1 pedido"
            else:
                texto_qtd_horario = f"{quantidade_horario} pedidos"

            texto_horario = (
                f"{hora_inicial:02d}h às "
                f"{hora_final:02d}h\n"
                f"{texto_qtd_horario}"
            )

        else:
            texto_horario = "-"

        self.__cards_resumo["horario_pico" ].atualizar_valor(texto_horario)

        self._atualizar_produtos(resultado)

        for componente in ( self.__area_resultados.winfo_children()):
            componente.destroy()

        pedidos_resultado = resultado["pedidos"]

        if not pedidos_resultado:

            mensagem = ctk.CTkLabel(
                master=self.__area_resultados,
                text=("Nenhum pedido encontrado " "para o período informado."),
                text_color=Tema.C2
            )

            mensagem.grid(row=0, column=0,  padx=20, pady=20, sticky="w")

            return

        for linha, pedido in enumerate(pedidos_resultado):
            CardRelatorio(master=self.__area_resultados, pedido=pedido, linha=linha)

    def _gerar_relatorio(self):

        tipo = self.__seletor_tipo.get()
        periodo = self.__entrada_periodo.get().strip()
        self.__callback_gerar_relatorio(tipo, periodo)

    def _atualizar_produtos(
        self,
        resultado
    ):

        for componente in (
            self.__area_produtos_vendidos
            .winfo_children()
        ):
            componente.destroy()

        for componente in (
            self.__area_ranking_produtos
            .winfo_children()
        ):
            componente.destroy()

        produtos_vendidos = resultado.get(
            "produtos_vendidos",
            []
        )

        ranking_produtos = resultado.get(
            "ranking_produtos",
            []
        )

        quantidade_total = resultado.get(
            "quantidade_total_produtos",
            0
        )

        quantidade_distintos = resultado.get(
            "quantidade_produtos_distintos",
            0
        )

        if not produtos_vendidos:

            mensagem_produtos = ctk.CTkLabel(
                master=self.__area_produtos_vendidos,
                text=(
                    "Nenhum produto encontrado "
                    "no período."
                ),
                text_color=Tema.C2
            )

            mensagem_produtos.grid(
                row=0,
                column=0,
                sticky="w",
                padx=20,
                pady=20
            )

            mensagem_ranking = ctk.CTkLabel(
                master=self.__area_ranking_produtos,
                text=(
                    "Não existem produtos "
                    "para formar o ranking."
                ),
                text_color=Tema.C2
            )

            mensagem_ranking.grid(
                row=0,
                column=0,
                sticky="w",
                padx=20,
                pady=20
            )

            return

        if quantidade_total == 1:

            texto_total_produtos = (
                "1 unidade vendida"
            )

        else:

            texto_total_produtos = (
                f"{quantidade_total} unidades vendidas"
            )

        if quantidade_distintos == 1:

            texto_produtos_distintos = (
                "1 produto diferente"
            )

        else:

            texto_produtos_distintos = (
                f"{quantidade_distintos} produtos diferentes"
            )

        resumo = ctk.CTkLabel(
            master=self.__area_produtos_vendidos,
            text=(
                f"{texto_total_produtos}\n"
                f"{texto_produtos_distintos}"
            ),
            text_color=Tema.C2,
            justify="left",
            anchor="w",
            font=ctk.CTkFont(
                size=14,
                weight="bold"
            )
        )

        resumo.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(15, 20)
        )

        for linha, produto in enumerate(
            produtos_vendidos,
            start=1
        ):

            quantidade = produto.get(
                "quantidade",
                0
            )

            if quantidade == 1:

                texto_quantidade = (
                    "1 unidade"
                )

            else:

                texto_quantidade = (
                    f"{quantidade} unidades"
                )

            nome_produto = produto.get(
                "nome",
                "Produto sem nome"
            )

            texto_produto = (
                f"{nome_produto}    "
                f"{texto_quantidade}"
            )

            label_produto = ctk.CTkLabel(
                master=self.__area_produtos_vendidos,
                text=texto_produto,
                text_color=Tema.C2,
                justify="left",
                anchor="w",
                font=ctk.CTkFont(
                    size=14
                )
            )

            label_produto.grid(
                row=linha,
                column=0,
                sticky="ew",
                padx=20,
                pady=8
            )

        for indice, produto in enumerate(
            ranking_produtos,
            start=1
        ):

            posicao_ranking = produto.get(
                "posicao",
                indice
            )

            quantidade = produto.get(
                "quantidade",
                0
            )

            if quantidade == 1:

                texto_unidades = (
                    "1 unidade vendida"
                )

            else:

                texto_unidades = (
                    f"{quantidade} unidades vendidas"
                )

            nome_produto = produto.get(
                "nome",
                "Produto sem nome"
            )

            texto_ranking = (
                f"{posicao_ranking}º  "
                f"{nome_produto}\n"
                f"{texto_unidades}"
            )

            label_ranking = ctk.CTkLabel(
                master=self.__area_ranking_produtos,
                text=texto_ranking,
                text_color=Tema.C2,
                justify="left",
                anchor="w",
                font=ctk.CTkFont(
                    size=14,
                    weight=(
                        "bold"
                        if posicao_ranking <= 3
                        else "normal"
                    )
                )
            )

            label_ranking.grid(
                row=indice - 1,
                column=0,
                sticky="ew",
                padx=20,
                pady=10
            )
