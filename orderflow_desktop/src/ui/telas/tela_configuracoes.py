import customtkinter as ctk
from dudoce_impressao_py.src.ui.tema import Tema


class TelaConfiguracoes(ctk.CTkFrame):
    
    def __init__(self, master, configuracoes, impressoras, callback_salvar, 
                 callback_testar_som, callback_testar_impressao, callback_atualizar_impressoras):

        super().__init__(master=master, fg_color="transparent")

        self.__configuracoes = configuracoes
        self.__impressoras = (impressoras if impressoras is not None else [])
        self.__callback_salvar = callback_salvar
        self.__callback_testar_som = callback_testar_som
        self.__callback_testar_impressao = callback_testar_impressao
        self.__callback_atualizar_impressoras = callback_atualizar_impressoras
       

        self.grid_columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self._criar_componentes()
        self.carregar_configuracoes_na_tela(self.__configuracoes)

    def _criar_componentes(self):

        titulo = ctk.CTkLabel(master=self, text="Configurações", text_color=Tema.C1, font=ctk.CTkFont(size=28, weight="bold"))
        titulo.grid(row=0, column=0, padx=30, pady=(25, 20), sticky="w")

        self.__frame_conteudo = ctk.CTkScrollableFrame(master=self, fg_color=Tema.C1, corner_radius=10, border_width=1, border_color=Tema.BORDA)
        self.__frame_conteudo.grid(row=1, column=0, sticky="nsew", padx=30, pady=(0,25))
        self.__frame_conteudo.grid_columnconfigure(1, weight=1)

        self._criar_secao_som()
        self._criar_secao_impressao()
        self._criar_secao_desenvolvedor()
        self._criar_botao_salvar()

    def _criar_titulo_secao(self, texto, linha):

        label = ctk.CTkLabel(master=self.__frame_conteudo, text=texto, text_color=Tema.C2, font=ctk.CTkFont(size=22, weight="bold"))
        label.grid(row=linha, column=0, columnspan=2, padx=20, pady=(25, 10), sticky="w")

    def _criar_label(self, texto, linha):

        label = ctk.CTkLabel(master=self.__frame_conteudo, text=texto, text_color=Tema.C2, font=ctk.CTkFont(size=15, weight="bold"))
        label.grid(row=linha, column=0, sticky="w", padx=25, pady=10)

        return label

    def _criar_entrada(self, linha, placeholder=""):

        entrada = ctk.CTkEntry(master=self.__frame_conteudo,placeholder_text=placeholder, fg_color=Tema.C2, text_color=Tema.TEXTO_ESCURO, border_color=Tema.BORDA)
        entrada.grid(row=linha, column=1, sticky="ew", padx=25, pady=10)

        return entrada
    
    def _criar_secao_som(self):

        self._criar_titulo_secao("Som", 0)
        self._criar_label("Som ativo:", 1)

        frame_som = ctk.CTkFrame(master=self.__frame_conteudo, fg_color="transparent")
        frame_som.grid(row=1, column=1, sticky="w", padx=25, pady=10)

        self.__switch_som = ctk.CTkSwitch(master=frame_som, text="Ativar som de novo pedido", text_color=Tema.C2, progress_color=Tema.C2, button_color=Tema.C3, button_hover_color=Tema.BORDA)
        self.__switch_som.grid(row=0, column=0, sticky="w", padx=25, pady=10)

        botao_testar_som = ctk.CTkButton(master=frame_som, text="Testar Som", width=120, text_color=Tema.C1, fg_color=Tema.C2, hover_color=Tema.C3, command= self.__callback_testar_som)
        botao_testar_som.grid(row=0, column=1)

    def _criar_secao_impressao(self):

        self._criar_titulo_secao("Impressão", 2)
        self._criar_label("Tipo de impressora:", 3)

        self.__seletor_tipo_impressora = (ctk.CTkOptionMenu(master=self.__frame_conteudo, values=["Normal", "Térmica"], fg_color=Tema.C2, button_color=Tema.C3, button_hover_color=Tema.BORDA, text_color=Tema.TEXTO_ESCURO, command=(self._alterar_tipo_impressora)))
        self.__seletor_tipo_impressora.grid(row=3, column=1, sticky="w", padx=25, pady=10)

        self._criar_label("Impressora:", 4)

        frame_selecao_impressora = (ctk.CTkFrame(master=self.__frame_conteudo, fg_color="transparent"))

        frame_selecao_impressora.grid(row=4, column=1, sticky="ew", padx=25, pady=10)

        frame_selecao_impressora\
            .grid_columnconfigure(0, weight=1)

        valores_impressoras = (self.__impressoras if self.__impressoras  else ["Nenhuma impressora encontrada"])

        self.__seletor_impressora = (ctk.CTkOptionMenu(master=frame_selecao_impressora, values=valores_impressoras, fg_color=Tema.C2, button_color=Tema.C3, button_hover_color=Tema.BORDA, text_color=Tema.TEXTO_ESCURO, width=360))
        self.__seletor_impressora.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        botao_atualizar_impressoras = (ctk.CTkButton(master=frame_selecao_impressora, text="Atualizar lista", width=130, text_color=Tema.C1, fg_color=Tema.C2, hover_color=Tema.C3,  command=(self.__callback_atualizar_impressoras)))
        botao_atualizar_impressoras.grid( row=0, column=1)

        self.__label_largura_papel = (self._criar_label("Largura da bobina:", 5))
        self.__seletor_largura_papel = (ctk.CTkOptionMenu(master=self.__frame_conteudo, values=["80 mm", "58 mm"], fg_color=Tema.C2, button_color=Tema.C3,  button_hover_color=Tema.BORDA, text_color=Tema.TEXTO_ESCURO))
        self.__seletor_largura_papel.grid(row=5, column=1, sticky="w", padx=25,  pady=10)

        self._criar_label("Quantidade de vias:", 6)

        self.__seletor_quantidade_vias = (ctk.CTkOptionMenu(master=self.__frame_conteudo, values=["1", "2", "3"], fg_color=Tema.C2, button_color=Tema.C3, button_hover_color=Tema.BORDA, text_color=Tema.TEXTO_ESCURO))
        self.__seletor_quantidade_vias.grid(row=6, column=1, sticky="w", padx=25, pady=10)

        botao_testar_impressao = (ctk.CTkButton(master=self.__frame_conteudo, text="Testar impressão", text_color=Tema.C1, fg_color=Tema.C2,  hover_color=Tema.C3, command=self._testar_impressao))
        botao_testar_impressao.grid(row=7, column=1, sticky="w", padx=25,  pady=(10, 20))

    def _criar_secao_desenvolvedor(self):

        self._criar_titulo_secao("Sobre o sistema", 8)

        texto_sistema = (
            "Dudôce — Sistema de Pedidos\n"
            "Versão 1.0\n\n"
            "Desenvolvido por Andrei Rodrigues\n"
            "Python e CustomTkinter"
        )

        label_sistema = ctk.CTkLabel(master=self.__frame_conteudo, text=texto_sistema, text_color=Tema.C2, justify="left", anchor="w", font=ctk.CTkFont(size=15))
        label_sistema.grid(row=9, column=0, columnspan=2, sticky="ew", padx=25, pady=(5, 20))

    def _criar_botao_salvar(self):

        self.__botao_salvar = ctk.CTkButton(master=self.__frame_conteudo, text="Salvar Configurações", text_color=Tema.C1, fg_color=Tema.C2, hover_color=Tema.C3, command=self._salvar_configuracoes)
        self.__botao_salvar.grid(row=10, column=0, columnspan=2, sticky="ew", padx=25, pady=(25, 30))

    def _limpar_entrada(self, entrada):

        entrada.delete(0, "end")

    def _preencher_entrada(self, entrada, valor):
        
        self._limpar_entrada(entrada)
        entrada.insert(0, str(valor))

    def _alterar_tipo_impressora(self, tipo):

        if tipo == "Térmica":
            self.__label_largura_papel.grid()
            self.__seletor_largura_papel.grid()

        else:
            self.__label_largura_papel.grid_remove()
            self.__seletor_largura_papel.grid_remove()

    def atualizar_impressoras(self, impressoras):

        self.__impressoras = (impressoras if isinstance(impressoras, list) else [])

        valores_impressoras = (self.__impressoras if self.__impressoras else ["Nenhuma impressora encontrada"])

        impressora_atual = (self.__seletor_impressora.get())

        impressora_salva = (self.__configuracoes.get("impressora", ""))

        self.__seletor_impressora.configure(values=valores_impressoras)

        if (impressora_atual in self.__impressoras):
            self.__seletor_impressora.set(impressora_atual)

        elif (impressora_salva in self.__impressoras ):
            self.__seletor_impressora.set(impressora_salva)

        elif self.__impressoras:
            self.__seletor_impressora.set(self.__impressoras[0])

        else:
            self.__seletor_impressora.set("Nenhuma impressora encontrada")

    def carregar_configuracoes_na_tela( self, configuracoes):

        self.__configuracoes = dict(configuracoes)

        som_ativo = configuracoes.get("som_ativo", True)

        if som_ativo:
            self.__switch_som.select()

        else:
            self.__switch_som.deselect()

        tipo_impressora = str(configuracoes.get("tipo_impressora", "normal")).strip().lower()

        if tipo_impressora == "termica":
            tipo_exibido = "Térmica"

        else:
            tipo_exibido = "Normal"

        self.__seletor_tipo_impressora.set(tipo_exibido)

        largura_papel = str(configuracoes.get("largura_papel", "80")).replace("mm", "").strip()

        if largura_papel not in ("58", "80"):
            largura_papel = "80"

        self.__seletor_largura_papel.set(f"{largura_papel} mm")

        self._alterar_tipo_impressora(tipo_exibido)


        impressora_salva = configuracoes.get("impressora", "")

        if (impressora_salva and impressora_salva in self.__impressoras):

            self.__seletor_impressora.set(impressora_salva)

        elif self.__impressoras:

            self.__seletor_impressora.set(self.__impressoras[0])

        else:

            self.__seletor_impressora.set("Nenhuma impressora encontrada")

        quantidade_vias = configuracoes.get( "quantidade_vias", 1)

        self.__seletor_quantidade_vias.set(str(quantidade_vias))

    def _salvar_configuracoes(self):

        tipo_selecionado = (self.__seletor_tipo_impressora.get())

        if tipo_selecionado == "Normal":
            tipo_impressora = "normal"

        else:
            tipo_impressora = "termica"

        nome_impressora = (self.__seletor_impressora.get())

        if nome_impressora == ("Nenhuma impressora encontrada" ):
            nome_impressora = ""

        largura_papel = (self.__seletor_largura_papel.get().replace("mm", "").strip())

        configuracoes = {
            "som_ativo": bool(self.__switch_som.get()),
            "tipo_impressora": tipo_impressora,
            "impressora": nome_impressora,
            "quantidade_vias": int( self.__seletor_quantidade_vias.get()),
            "largura_papel": largura_papel
        }

        self.__callback_salvar(configuracoes)

    def _testar_impressao(self):

        tipo_selecionado = ( self.__seletor_tipo_impressora.get())

        if tipo_selecionado == "Normal":
            tipo_impressora = "normal"

        else:
            tipo_impressora = "termica"

        nome_impressora = (self.__seletor_impressora.get())

        if nome_impressora == ("Nenhuma impressora encontrada"):
            nome_impressora = ""

        quantidade_vias = int(self.__seletor_quantidade_vias.get())

        largura_papel = (self.__seletor_largura_papel.get().replace("mm", "").strip())

        self.__callback_testar_impressao(nome_impressora, tipo_impressora, quantidade_vias, largura_papel)





