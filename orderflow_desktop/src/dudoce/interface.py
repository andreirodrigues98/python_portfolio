import customtkinter as ctk
from datetime import datetime
from zoneinfo import ZoneInfo

from dudoce_impressao_py.src.dudoce.caminhos import (obter_caminho_configuracao, obter_caminho_credencial)

from dudoce_impressao_py.src.modelos.pedido import Pedido
from dudoce_impressao_py.src.controladores.gerenciador_pedidos import GerenciadorPedidos
from dudoce_impressao_py.src.ui.cards.card_pedido import CardPedido

from dudoce_impressao_py.src.servicos.firebase_service import FirebaseService
from dudoce_impressao_py.src.servicos.som_service import SomService

from dudoce_impressao_py.src.ui.telas.tela_historico import TelaHistorico
from dudoce_impressao_py.src.ui.telas.tela_configuracoes import TelaConfiguracoes
from dudoce_impressao_py.src.ui.telas.tela_relatorios import TelaRelatorios
from dudoce_impressao_py.src.ui.tema import Tema
from dudoce_impressao_py.src.servicos.relatorio_service import RelatorioService
from dudoce_impressao_py.src.servicos.configuracao_service import ConfiguracaoService
from dudoce_impressao_py.src.servicos.impressora_service import ImpressoraService


class AplicacaoDudoce(ctk.CTk):
    
    def __init__(self, titulo, largura, altura):
        super().__init__()

        self.__titulo = titulo
        self.__largura = largura
        self.__altura =  altura
        

        self.__gerenciador = GerenciadorPedidos()
        self.__som_service = SomService()
        self.__relatorio_service = RelatorioService()
        self.__impressora_service = ImpressoraService()

        self.__documentos_carregados = set()
        self.__observador_firebase = None

        caminho_credencial = (obter_caminho_credencial())
        caminho_configuracoes = (obter_caminho_configuracao())
        
        self.__configuracao_service = ConfiguracaoService(caminho_arquivo=caminho_configuracoes)
        self.__configuracoes = (self.__configuracao_service.carregar_configuracoes())

        self.__som_service.definir_ativado(self.__configuracoes.get("som_ativo", True))
        self.__firebase = FirebaseService(caminho_credencial=str(caminho_credencial), nome_colecao="orders")

        try:
            self.__impressoras = (self.__impressora_service.listar_impressoras())

        except Exception as erro:

            print("Erro ao listar impressoras:",erro)

            self.__impressoras = []

        self.__telas = []
        self.__cards_pedidos = {}

        self._configurar_janela()
        self._criar_sidebar()
        self._criar_cabecalho()
        self._criar_area_pedidos()
        self._criar_telas_secundarias()
        self._iniciar_escuta_firebase()
    
    def _criar_telas_secundarias(self):

        self.__tela_historico = TelaHistorico(master=self, callback_reimprimir=self._reimprimir_pedido_historico)
        self.__tela_configuracoes = TelaConfiguracoes(master=self, configuracoes=self.__configuracoes, impressoras=self.__impressoras, callback_salvar=self._salvar_configuracoes,
                                                      callback_testar_som=self._testar_som, callback_testar_impressao=self._testar_impressao, callback_atualizar_impressoras=(self._atualizar_lista_impressoras))
        self.__tela_relatorios = TelaRelatorios(master=self, callback_gerar_relatorio=self._gerar_relatorio)

        telas_secundarias = [self.__tela_historico, self.__tela_configuracoes, self.__tela_relatorios]

        for tela in telas_secundarias:
            tela.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

            self.__telas.append(tela)

            tela.grid_remove()

    def _configurar_janela(self):

        self.title(self.__titulo)
        self.geometry(f"{self.__largura}x{self.__altura}")
        self.minsize(900,600) # largura_minina, altura_minima

        self.configure(fg_color=Tema.FUNDO_PRINCIPAL)

        self.grid_rowconfigure(1, weight=1) # indice, weight
        self.grid_columnconfigure(1, weight=1) # indice, weight

        self.protocol("WM_DELETE_WINDOW", self._fechar_aplicacao)

    def _criar_sidebar(self):

        self.__sidebar = ctk.CTkFrame(master=self, width=220, corner_radius=0, fg_color=Tema.FUNDO_SIDEBAR)
        self.__sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        self.__sidebar.grid_propagate(False)

        titulo = ctk.CTkLabel(master=self.__sidebar, text="DUDÔCE", text_color=Tema.TEXTO_CLARO, font=ctk.CTkFont(size=24, weight="bold"))
        titulo.grid(row=0, column=0, padx=20, pady=(30,40))

        botao_pedidos = ctk.CTkButton(master=self.__sidebar, text="Pedidos", command=self._mostrar_tela_pedidos, fg_color=Tema.BOTAO, hover_color=Tema.BOTAO_HOVER, text_color=Tema.TEXTO_CLARO, border_width=1, border_color=Tema.C2)
        botao_pedidos.grid(row=1, column=0, sticky="ew", padx=20, pady=8)

        botao_historico = ctk.CTkButton(master=self.__sidebar, text="Histórico", command=self._mostrar_tela_historico, fg_color=Tema.BOTAO, hover_color=Tema.BOTAO_HOVER, text_color=Tema.TEXTO_CLARO, border_width=1, border_color=Tema.C2)
        botao_historico.grid(row=2, column=0, sticky="ew", padx=20, pady=8)

        botao_relatorios = ctk.CTkButton(master=self.__sidebar, text="Relatórios", command=self._mostrar_tela_relatorios, fg_color=Tema.BOTAO, hover_color=Tema.BOTAO_HOVER, text_color=Tema.TEXTO_CLARO, border_width=1, border_color=Tema.C2)
        botao_relatorios.grid(row=3, column=0, sticky="ew", padx=20, pady=8)

        botao_configuracoes = ctk.CTkButton(master=self.__sidebar, text="Configurações", command=self._mostrar_tela_configuracoes, fg_color=Tema.BOTAO, hover_color=Tema.BOTAO_HOVER, text_color=Tema.TEXTO_CLARO, border_width=1, border_color=Tema.C2)
        botao_configuracoes.grid(row=4, column=0, sticky="ew", padx=20, pady=8)

    def _mostrar_tela(self, tela):

        for tela_registrada in self.__telas:
            tela_registrada.grid_remove()
        
        tela.grid()

    def _mostrar_tela_pedidos(self):

        self._mostrar_tela(self.__tela_pedidos)

    def _mostrar_tela_historico(self):

        try:

            pedidos = self.__firebase.buscar_pedidos()

            self.__tela_historico.atualizar_pedidos(pedidos)
            self._mostrar_tela(self.__tela_historico)

            self._atualizar_status(f"Histórico carregado — {len(pedidos)} pedidos encontrados.")

        except Exception as erro:

            print("Erro ao carregar histórico:", erro)

            self._atualizar_status("Não foi possível carregar o histórico.")

    def _mostrar_tela_relatorios(self):

        self._mostrar_tela(self.__tela_relatorios)

    def _mostrar_tela_configuracoes(self):

        self._mostrar_tela(self.__tela_configuracoes)

    def _criar_cabecalho(self):
        cabecalho = ctk.CTkFrame(master=self, height=80, corner_radius=0, fg_color=Tema.FUNDO_CABECALHO, border_width=1, border_color=Tema.BORDA) # onde fica, altura desejada, sem arredondamentos
        cabecalho.grid(row=0, column=1, sticky="ew") # e --> direita, w --> esquerda
        cabecalho.grid_columnconfigure(0, weight=1)

        titulo_cabecalho = ctk.CTkLabel(master=cabecalho, text="DUDÔCE — PEDIDOS DO DIA", text_color=Tema.C1, font=ctk.CTkFont(size= 24, weight="bold"))
        titulo_cabecalho.grid(row=0, column=0, padx=25, pady=20, sticky="w")

        self.__status_sistema = ctk.CTkLabel(master=cabecalho, text="Sistema Iniciado - aguardando novos pedidos", text_color=Tema.TEXTO_SECUNDARIO, font=ctk.CTkFont(size=14))
        self.__status_sistema.grid(row=0, column=1, padx=25, pady=20, sticky="e")

    def _criar_area_pedidos(self):
        self.__tela_pedidos = ctk.CTkFrame(master=self, fg_color="transparent")
        # n → cima
        # s → baixo
        # e → direita
        # w → esquerda
        self.__tela_pedidos.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

        self.__tela_pedidos.grid_columnconfigure(0, weight=1)
        self.__tela_pedidos.grid_columnconfigure(1, weight=1)
        self.__tela_pedidos.grid_rowconfigure(0, weight=1)

        

        self.__titulo_nao_impressos, self.__lista_nao_impressos, self.__mensagem_nao_impressos = self._criar_coluna_pedidos(master=self.__tela_pedidos, numero_coluna=0, titulo_coluna="Não Impressos (0)", mensagem_vazia="Nenhum pedido aguardando impressão.")
        self.__titulo_impressos, self.__lista_impressos, self.__mensagem_impressos = self._criar_coluna_pedidos(master=self.__tela_pedidos, numero_coluna=1, titulo_coluna="Impressos (0)", mensagem_vazia="Nenhum pedido foi impresso hoje.")
      
    def _criar_coluna_pedidos(self, master, numero_coluna, titulo_coluna, mensagem_vazia):
        
        frame_coluna = ctk.CTkFrame(master=master, fg_color=Tema.FUNDO_SIDEBAR)
        frame_coluna.grid(row=0, column = numero_coluna, sticky="nsew", padx=10)
        frame_coluna.grid_columnconfigure(0, weight=1)
        frame_coluna.grid_rowconfigure(1, weight=1)

        label_titulo = ctk.CTkLabel(master= frame_coluna, text=titulo_coluna, text_color=Tema.TEXTO_CLARO, font=ctk.CTkFont(size=24, weight="bold"))
        label_titulo.grid(row=0, column=0, padx=25, pady=20, sticky="w")

        lista_pedidos = ctk.CTkScrollableFrame(master=frame_coluna, fg_color=Tema.C2)
        lista_pedidos.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        lista_pedidos.grid_columnconfigure(0, weight=1) 

        label_mensagem_vazia = ctk.CTkLabel(master=lista_pedidos, text=mensagem_vazia, text_color=Tema.FUNDO_SIDEBAR)
        label_mensagem_vazia.grid(row=0, column=0, padx=25, pady=20, sticky="w")

        return label_titulo, lista_pedidos, label_mensagem_vazia
  
    def _obter_proxima_linha(self, master):

        linhas_ocupadas = []

        for widget in master.grid_slaves():
            informacoes_grid = widget.grid_info()
            
            if "row" in informacoes_grid:
                linhas_ocupadas.append(int(informacoes_grid["row"]))
        
        return max(linhas_ocupadas, default=0) + 1

    def criar_card_pedido(self, master, pedido, linha):

        card = CardPedido(master=master, pedido=pedido, linha=linha, callback_imprimir=self.imprimir_pedido, callback_reimprimir=self.reimprimir_pedido)

        self.__cards_pedidos[pedido.documento_id] = card

        return card

    def _definir_pedido_processando(self, pedido, processando):

        documento_id = pedido.documento_id

        card = self.__cards_pedidos.get(documento_id)

        if card is None:
            return

        try:
            card.definir_processando(processando)

        except Exception as erro:
            print("Erro ao alterar botão de impressão:", repr(erro))

    @staticmethod
    def _formatar_quantidade_vias(quantidade):

        try:
            quantidade = int(quantidade)

        except (TypeError, ValueError):
            quantidade = 1

        if quantidade == 1:
            return "1 via"

        return f"{quantidade} vias"

    @staticmethod
    def _obter_mensagem_erro(erro):

        causa = (erro.__cause__ if erro.__cause__ is not None else erro)

        mensagem = str(causa).strip()

        if not mensagem:
            mensagem = str(erro).strip()

        if not mensagem:
            mensagem = ("Erro desconhecido durante ""a impressão.")

        return mensagem

    def _imprimir_pedido_fisicamente(self, pedido, tipo_copia):

        configuracoes = dict(self.__configuracoes)

        quantidade_vias = (self.__impressora_service.imprimir_pedido(pedido=pedido, configuracoes=configuracoes, tipo_copia=tipo_copia))

        return quantidade_vias

    def _registrar_impressao_local(self, pedido):

        self.__gerenciador.imprimir_pedido(pedido)

        documento_id = pedido.documento_id

        card_antigo = (self.__cards_pedidos.pop(documento_id, None))

        if card_antigo is not None:
            card_antigo.destroy()

        linha = self._obter_proxima_linha(self.__lista_impressos)

        self.criar_card_pedido(master=self.__lista_impressos, pedido=pedido, linha=linha)

        self._atualizar_interface()

    def imprimir_pedido(self, pedido):
        self._definir_pedido_processando(pedido, True)

        try:
            quantidade_vias = (self._imprimir_pedido_fisicamente(pedido=pedido, tipo_copia="original"))

        except Exception as erro:
            mensagem_erro = (self._obter_mensagem_erro(erro))
            print("Erro ao imprimir pedido:", repr(erro))
            self._definir_pedido_processando(pedido, False)
            self._atualizar_status(f"Pedido #{pedido.numero} não foi impresso — {mensagem_erro}")
            return

        try:
            self._registrar_impressao_local(pedido)

        except Exception as erro:
            print("O pedido foi impresso, mas ocorreu erro na atualização local:", repr(erro))
            self._atualizar_status(f"ATENÇÃO: pedido #{pedido.numero} foi impresso fisicamente, mas a tela não foi atualizada. Não imprima novamente.")
            return

        try:
            self.__firebase.marcar_pedido_como_impresso(pedido.documento_id)

        except Exception as erro:
            print("Pedido impresso, mas não registrado no Firebase:", repr(erro))
            self._atualizar_status(f"ATENÇÃO: pedido #{pedido.numero} foi impresso, mas não foi sincronizado com o Firebase. Não imprima novamente.")
            return

        texto_vias = (self._formatar_quantidade_vias(quantidade_vias))
        self._atualizar_status(f"Pedido #{pedido.numero} impresso com sucesso — {texto_vias}.")

    def reimprimir_pedido(self, pedido):
        self._definir_pedido_processando(pedido, True)

        try:
            quantidade_vias = (self._imprimir_pedido_fisicamente(pedido=pedido, tipo_copia="reimpressao"))

        except Exception as erro:
            mensagem_erro = (self._obter_mensagem_erro(erro))
            print("Erro ao reimprimir pedido:", repr(erro))
            self._definir_pedido_processando(pedido, False)
            self._atualizar_status(f"Pedido #{pedido.numero} não foi reimpresso — {mensagem_erro}")
            return

        self.__gerenciador.reimprimir_pedido(pedido)
        card = self.__cards_pedidos.get(pedido.documento_id)

        if card is not None:
            card.atualizar_reimpressao()
            card.definir_processando(False)

        try:
            self.__firebase.registrar_reimpressao(pedido.documento_id)

        except Exception as erro:
            print("Reimpressão realizada, mas não registrada no Firebase:", repr(erro))
            self._atualizar_status(f"ATENÇÃO: pedido #{pedido.numero} foi reimpresso, mas o Firebase não foi atualizado.")
            return

        texto_vias = (self._formatar_quantidade_vias(quantidade_vias))
        self._atualizar_status(f"Pedido #{pedido.numero} reimpresso com sucesso — {texto_vias}; {pedido.texto_reimpressao}.")

    def _atualizar_contadores(self):

        qtd_nao_impresso = self.__gerenciador.quantidade_nao_impressos()
        qtd_impresso = self.__gerenciador.quantidade_impressos()
        
        self.__titulo_nao_impressos.configure(text=f"Não Impressos ({qtd_nao_impresso})")
        self.__titulo_impressos.configure(text=f"Impressos ({qtd_impresso})")

    def _atualizar_mensagens_vazias(self):

        if self.__gerenciador.quantidade_nao_impressos() == 0:
            self.__mensagem_nao_impressos.grid()
        else:
            self.__mensagem_nao_impressos.grid_remove()
        
        if self.__gerenciador.quantidade_impressos() == 0:
            self.__mensagem_impressos.grid()
        else:
            self.__mensagem_impressos.grid_remove()

    def _atualizar_status(self, mensagem):
        self.__status_sistema.configure(text=mensagem)

    def _atualizar_interface(self):
        self._atualizar_contadores()
        self._atualizar_mensagens_vazias()

    def _iniciar_escuta_firebase(self):

        try:
            self.__observador_firebase = (self.__firebase.escutar_pedidos(
                callback_alteracao=(self._receber_alteracao_firebase),
                    callback_erro=(self._receber_erro_firebase)
                )
            )

            self._atualizar_status("Aguardando novos pedidos.")

        except Exception as erro:
            self.__observador_firebase = None

            print("Erro ao iniciar listener do Firebase:", repr(erro))

            self._atualizar_status("Não foi possível conectar " "ao Firebase." )
    
    def _receber_alteracao_firebase(self, tipo_alteracao, pedido, carga_inicial):

        try:
            self.after( 0, lambda: (self._processar_alteracao_firebase(tipo_alteracao, pedido, carga_inicial)))

        except Exception:
            return

    def _receber_erro_firebase(self, erro):

        try:
            self.after(0, lambda erro_recebido=erro: (self._tratar_erro_firebase(erro_recebido)))

        except Exception:
            return

    def _tratar_erro_firebase(self, erro):

        print("Erro recebido do Firebase:", repr(erro))

        self._atualizar_status("Um pedido inválido foi ignorado. " "O sistema continua funcionando." )

    def _adicionar_pedido_firebase(self, pedido, carga_inicial):

        if not self._pedido_eh_de_hoje(pedido):
            return 
        
        documento_id = pedido.documento_id

        if documento_id in self.__documentos_carregados:
            return

        self.__documentos_carregados.add(documento_id)

        self.__gerenciador.adicionar_pedido(pedido)

        if pedido.foi_impresso:
            lista_destino = self.__lista_impressos
        else:
            lista_destino = self.__lista_nao_impressos

        if carga_inicial:

            linha = self._obter_proxima_linha(lista_destino)

        else:

            self._abrir_espaco_no_topo(lista_destino)

            linha = 1

       
        card = self.criar_card_pedido(master=lista_destino, pedido=pedido, linha=linha)

        self._atualizar_interface()

        if not carga_inicial and not pedido.foi_impresso:

            card.destacar_novo_pedido()

            if self.__configuracoes.get("som_ativo", True):

                self.__som_service.tocar_novo_pedido()
            
            self._atualizar_status(f"Novo pedido #{pedido.numero} recebido ""— aguardando impressão!")

    def _fechar_aplicacao(self):

        if self.__observador_firebase is not None:
            try:
                self.__observador_firebase.unsubscribe()

            except Exception as erro:
                print("Erro ao encerrar listener:", repr(erro))

            finally:
                self.__observador_firebase = None

        self.destroy()

    def _processar_alteracao_firebase(self, tipo_alteracao, pedido, carga_inicial):

        if tipo_alteracao == "ADDED":

            self._adicionar_pedido_firebase(pedido, carga_inicial)

        elif tipo_alteracao == "MODIFIED":

            self._atualizar_pedido_firebase(pedido)

        elif tipo_alteracao == "REMOVED":

            self._remover_pedido_firebase(pedido)

    def _atualizar_pedido_firebase(self, pedido):

        documento_id = pedido.documento_id

        if documento_id:
            self.__documentos_carregados.add(documento_id)

        if not self._pedido_eh_de_hoje(pedido):
            self.__gerenciador.remover_pedido(documento_id)
            
            card_antigo = self.__cards_pedidos.pop(documento_id, None)

            if card_antigo is not None:
                card_antigo.destroy()

            self.__documentos_carregados.discard(documento_id)

            self._atualizar_interface()

            return 

        self.__gerenciador.atualizar_pedido(pedido)

        card_antigo = self.__cards_pedidos.pop(documento_id, None)

        if card_antigo is not None:
            card_antigo.destroy()

        if pedido.foi_impresso:
            lista_destino = self.__lista_impressos
        else:
            lista_destino = self.__lista_nao_impressos

        linha = self._obter_proxima_linha(lista_destino)

        self.criar_card_pedido(master=lista_destino, pedido=pedido, linha=linha)

        self._atualizar_interface()

    def _remover_pedido_firebase(self, pedido):

        documento_id = pedido.documento_id

        self.__gerenciador.remover_pedido(documento_id)

        card = self.__cards_pedidos.pop(documento_id, None)

        if card is not None:
            card.destroy()

        self.__documentos_carregados.discard(documento_id)

        self._atualizar_interface()

        self._atualizar_status(f"Pedido #{pedido.numero} removido do Firebase.")

    def _abrir_espaco_no_topo(self, lista_pedidos):

        for widget in lista_pedidos.grid_slaves():

            if not isinstance(widget, CardPedido):
                continue

            informacoes_grid = widget.grid_info()

            linha_atual = int(informacoes_grid["row"])

            widget.grid_configure(row=linha_atual + 1)

    def _pedido_eh_de_hoje(self, pedido):

        hoje = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y")

        return pedido.data_pedido == hoje

    def _reimprimir_pedido_historico(self, pedido):
        try:
            quantidade_vias = (self._imprimir_pedido_fisicamente(pedido=pedido, tipo_copia="historico"))

        except Exception as erro:
            mensagem_erro = (self._obter_mensagem_erro(erro))
            print("Erro ao imprimir cópia do histórico:", repr(erro))
            self._atualizar_status(f"Pedido #{pedido.numero} não foi impresso pelo histórico — {mensagem_erro}")
            return

        pedido.registrar_copia_historico()
        self.__tela_historico.atualizar_pedido_reimpresso(pedido)

        try:
            self.__firebase.registrar_copia_historico(pedido.documento_id)

        except Exception as erro:
            print("Cópia impressa, mas não registrada no Firebase:", repr(erro))
            self._atualizar_status(f"ATENÇÃO: cópia do pedido #{pedido.numero} foi impressa, mas não foi sincronizada.")
            return

        texto_vias = (self._formatar_quantidade_vias(quantidade_vias))
        self._atualizar_status(f"Cópia do pedido #{pedido.numero} impressa pelo histórico — {texto_vias}.")

    def _gerar_relatorio(self, tipo, periodo):

        if not periodo:
            self._atualizar_status("Informe o período do relatório.")
            return

        try:
            pedidos = self.__firebase.buscar_pedidos()

            if tipo == "Diário":
                resultado = (self.__relatorio_service.gerar_relatorio_diario(pedidos, periodo))
            elif tipo == "Mensal":
                resultado = (self.__relatorio_service.gerar_relatorio_mensal(pedidos, periodo))
            elif tipo == "Anual":
                resultado = (self.__relatorio_service.gerar_relatorio_anual(pedidos, periodo))
            else:
                self._atualizar_status("Tipo de relatório inválido!")
                return
                
            
            self.__tela_relatorios.atualizar_relatorio(resultado)

            self._atualizar_status(f"Relatório {tipo.lower()} gerado com sucesso!")
        
        except ValueError as erro:
            self._atualizar_status(str(erro))
        except Exception as erro:
            self._atualizar_status("Não foi possível gerar o relatório!")

    def _salvar_configuracoes(self, configuracoes):

        try:

            self.__configuracoes = (
                self.__configuracao_service
                .salvar_configuracoes(
                    configuracoes
                )
            )

            som_ativo = self.__configuracoes.get(
                "som_ativo",
                True
            )

            self.__som_service.definir_ativado(
                som_ativo
            )

            self.__tela_configuracoes.carregar_configuracoes_na_tela(
                self.__configuracoes
            )

            self._atualizar_status(
                "Configurações salvas com sucesso!"
            )

        except Exception as erro:

            print(
                "Erro ao salvar configurações:",
                erro
            )

            self._atualizar_status(
                "Não foi possível salvar as configurações."
            )

    def _testar_som(self):

        try:
            self.__som_service.tocar_teste()

            self._atualizar_status(
                "Som reproduzido com sucesso."
            )

        except Exception as erro:

            print(
                "Erro ao testar som:",
                erro
            )

            self._atualizar_status(
                "Não foi possível reproduzir o som."
            )

    def _atualizar_lista_impressoras(self):

        try:
            impressoras = (self.__impressora_service.listar_impressoras())

            self.__impressoras = (impressoras)

            self.__tela_configuracoes\
                .atualizar_impressoras(
                    impressoras
                )

            quantidade = len(impressoras)

            if quantidade == 1:
                mensagem = ("1 impressora encontrada.")

            else:
                mensagem = (f"{quantidade} impressoras ""encontradas.")

            self._atualizar_status(mensagem)

        except Exception as erro:
            print("Erro ao atualizar impressoras:", repr(erro))

            self._atualizar_status("Não foi possível atualizar ""a lista de impressoras.")

    def _testar_impressao(self, nome_impressora, tipo_impressora, quantidade_vias, largura_papel):

        try:
            quantidade_impressa = (self.__impressora_service.imprimir_teste(
                    nome_impressora=(nome_impressora),
                    tipo_impressora=(tipo_impressora),
                    quantidade_vias=(quantidade_vias),
                    largura_papel=(largura_papel))
            )

            if quantidade_impressa == 1:
                texto_vias = "1 via"

            else:
                texto_vias = (f"{quantidade_impressa} vias")

            self._atualizar_status( "Teste enviado para a impressora " f"— {texto_vias}.")

        except Exception as erro:
            print("Erro ao testar impressão:", repr(erro))

            causa = (erro.__cause__ if erro.__cause__ is not None else erro)

            self._atualizar_status(str(causa))
