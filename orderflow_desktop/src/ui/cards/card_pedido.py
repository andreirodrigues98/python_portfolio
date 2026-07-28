import customtkinter as ctk
from dudoce_impressao_py.src.ui.tema import Tema

class CardPedido(ctk.CTkFrame):
    
    def __init__(self, master, pedido, linha, callback_imprimir, callback_reimprimir):

        super().__init__(master=master, fg_color=Tema.C1)

        self.__tarefa_destaque = None
        self.__borda_original = 0

        self.__pedido = pedido

        self.__callback_imprimir = callback_imprimir
        self.__callback_reimprimir = callback_reimprimir

        self.grid(row=linha, column=0, sticky="nsew", padx=20, pady=20)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self._criar_cabecalho()
        self._criar_nome()
        self._criar_itens()
        self._criar_total()
        self._criar_obs_pedido()
        linha_atual = self._criar_area_impressao()
        self._criar_linha_divisoria(linha_atual)

    def _criar_cabecalho(self):

        numero_pedido =(self.__pedido.numero or "Não informado")
        horario_pedido = (self.__pedido.horario or "Não informado")
        
        label_numero = ctk.CTkLabel(master=self, text=f"Pedido #{numero_pedido}", text_color=Tema.C2)
        label_numero.grid(row=0, column=0, sticky="w", padx=20, pady=20)

        label_horario = ctk.CTkLabel(master=self, text=horario_pedido, text_color=Tema.C2)
        label_horario.grid(row=0, column=1, sticky="e", padx=20, pady=20)

    def _criar_nome(self):
        nome = (self.__pedido.nome or "Cliente não informado")

        label_total_pedido = ctk.CTkLabel(master=self, text=f"Cliente: {nome}", text_color=Tema.C2, justify="left")
        label_total_pedido.grid(row=1, column=0, sticky="w", padx=20, pady=10)

    def _criar_itens(self):

        if self.__pedido.itens:
            texto_itens = "\n\n".join(self.__pedido.itens)
        else:
            texto_itens = "Nenhum item informado."

        label_texto_pedido = ctk.CTkLabel(master=self, text=texto_itens, text_color=Tema.C2, justify="left", anchor="w", wraplength=560)
        label_texto_pedido.grid(row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

    @staticmethod
    def _formatar_moeda(valor):

        try:
            valor = float(valor)

        except (TypeError, ValueError):
            valor = 0

        valor_formatado = (f"{valor:,.2f}".replace(",", "TEMP").replace(".", ",").replace("TEMP", "."))

        return f"R$ {valor_formatado}"

    def _criar_total(self):

        total_pedido_formatado = self._formatar_moeda(self.__pedido.total)

        label_total_pedido = ctk.CTkLabel(master=self, text=f"Total: {total_pedido_formatado}", text_color=Tema.C2, justify="left")
        label_total_pedido.grid(row=3, column=0, sticky="w", padx=20, pady=10)

    def _criar_obs_pedido(self):
        
        obs_pedido = self.__pedido.observacao or "Nenhuma observação."

        label_obs_pedido = ctk.CTkLabel(master=self, text=f"Observação: {obs_pedido}", text_color=Tema.C2, justify="left", anchor="w", wraplength=560)
        label_obs_pedido.grid(row=4, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

    def _criar_area_impressao(self):
        
        linha_atual = 5

        self.__label_impresso_em = ctk.CTkLabel(master=self, text="", text_color=Tema.C2)
        self.__label_reimpresso_em = ctk.CTkLabel(master=self, text="", text_color=Tema.C2)
        self.__label_quantidade_reimpressoes = ctk.CTkLabel(master=self, text="", text_color=Tema.C2)

        if self.__pedido.foi_impresso:

            self.__label_impresso_em.configure(text=f"Impresso em {self.__pedido.impresso_em}", text_color=Tema.C2)
            self.__label_impresso_em.grid(row=linha_atual, column=0, sticky="w", padx=20, pady=10)
            
            linha_atual += 1

            if self.__pedido.quantidade_reimpressoes > 0:
                
                self.__label_reimpresso_em.configure(text=f"Reimpresso em: {self.__pedido.ultima_reimpressao}", text_color=Tema.C2)
                self.__label_reimpresso_em.grid(row=linha_atual, column=0, columnspan=2, sticky="w", padx=20, pady=10)
                
                linha_atual += 1
                
                self.__label_quantidade_reimpressoes.configure(text=self.__pedido.texto_reimpressao, text_color=Tema.C2)
                self.__label_quantidade_reimpressoes.grid(row=linha_atual, column=0, columnspan=2, sticky="w", padx=20, pady=10)
                linha_atual += 1

            self.__botao_impresso = ctk.CTkButton(master=self, text="Reimprimir", text_color=Tema.C1, command=lambda: self.__callback_reimprimir(self.__pedido), fg_color=Tema.C2, hover_color=Tema.C3)
        else:
            self.__botao_impresso = ctk.CTkButton( master=self, text="Imprimir Pedido", text_color=Tema.C1, command=lambda: self.__callback_imprimir(self.__pedido), fg_color=Tema.C2, hover_color=Tema.C3)
            
        self.__botao_impresso.grid(row=linha_atual, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

        linha_atual +=1 

        return linha_atual

    def definir_processando(self, processando):

        if processando:
            self.__botao_impresso.configure(state="disabled", text="Imprimindo...")
            return

        if self.__pedido.foi_impresso:
            texto_botao = "Reimprimir"

        else:
            texto_botao = "Imprimir Pedido"

        self.__botao_impresso.configure(state="normal", text=texto_botao)

    def atualizar_reimpressao(self):

        if not self.__pedido.foi_impresso:
            return

        if not self.__label_impresso_em.winfo_manager():
            return

        linha_impresso = int(self.__label_impresso_em.grid_info()["row"])

        linha_reimpressao = (linha_impresso + 1)

        self.__label_reimpresso_em.configure(text=(f"Reimpresso em: {self.__pedido.ultima_reimpressao}"), text_color=Tema.C2 )

        self.__label_quantidade_reimpressoes.configure(text=self.__pedido.texto_reimpressao, text_color=Tema.C2)

        self.__label_reimpresso_em.grid(row=linha_reimpressao, column=0, columnspan=2, sticky="w", padx=20, pady=10 )

        self.__label_quantidade_reimpressoes.grid(row=linha_reimpressao + 1, column=0, columnspan=2, sticky="w", padx=20, pady=10)

        self.__botao_impresso.grid(row=linha_reimpressao + 2, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

        self.__linha_divisoria.grid(row=linha_reimpressao + 3, column=0, columnspan=2, sticky="ew", padx=20, pady=20)

    def atualizar_para_impresso(self):
        
        self.__label_impresso_em.configure(text=f"Impresso em {self.__pedido.impresso_em}")
        self.__label_impresso_em.grid(row=5, column=0, sticky="w", padx=20, pady=10)

        self.__botao_impresso.configure(text="Reimprimir", command=lambda: self.__callback_reimprimir(self.__pedido))
        self.__botao_impresso.grid(row=6, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

        self.__linha_divisoria.grid(row=7, column=0, columnspan=2, sticky="ew", padx=20, pady=20)

    def _criar_linha_divisoria(self, linha_atual):

        self.__linha_divisoria = ctk.CTkFrame(master=self, height=4, fg_color=Tema.C2)
        self.__linha_divisoria.grid(row=linha_atual, column=0, columnspan=2, sticky="ew", padx=20, pady=20)

    def destacar_novo_pedido(self):

        if self.__tarefa_destaque is not None:
            self.after_cancel(self.__tarefa_destaque)

        self.configure(border_width=4, border_color="#22C55E")

        self.__tarefa_destaque = self.after(7000, self._remover_destaque)

    def _remover_destaque(self):

        if self.winfo_exists():
            self.configure(border_width=0)

        self.__tarefa_destaque = None

    @property
    def numero_pedido(self):
        return self.__pedido.numero

