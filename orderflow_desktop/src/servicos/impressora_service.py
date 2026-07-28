import win32con
import win32print
import win32ui

from dudoce_impressao_py.src.servicos.comprovante_service import ComprovanteService

class ImpressoraService:

    def __init__(self):
        self.__comprovante_service = (ComprovanteService())

    def listar_impressoras(self):

        flags = (win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS)

        try:
            impressoras_encontradas = (win32print.EnumPrinters(flags, None, 1))

        except Exception as erro:

            raise RuntimeError("Não foi possível buscar as impressoras do Windows.") from erro
        
        nomes_impressoras = []

        for impressora in impressoras_encontradas:
            try:
                nome_impressora = str(impressora[2] or "").strip()

            except (IndexError, TypeError):
                continue

            if nome_impressora:
                nomes_impressoras.append(nome_impressora)

        return sorted(set(nomes_impressoras), key=str.casefold)

    @staticmethod
    def _normalizar_tipo_impressora(tipo_impressora):

        tipo_impressora = str(tipo_impressora or "normal").strip().lower()

        if tipo_impressora not in ("normal", "termica"):
            tipo_impressora = "normal"

        return tipo_impressora

    @staticmethod
    def _normalizar_quantidade_vias(quantidade_vias):

        try:
            quantidade_vias = int(quantidade_vias)

        except (TypeError, ValueError):
            quantidade_vias = 1

        return max(1, min(quantidade_vias, 3))

    @staticmethod
    def _normalizar_largura_papel(largura_papel):

        largura_papel = str(largura_papel or "80").replace("mm", "").strip()

        if largura_papel not in ("58", "80"):
            largura_papel = "80"

        return largura_papel

    @staticmethod
    def _validar_nome_impressora(nome_impressora):

        nome_impressora = str(nome_impressora or "").strip()

        if not nome_impressora:
            raise ValueError("Selecione uma impressora.")
        
        return nome_impressora

    def imprimir_teste(self, nome_impressora, tipo_impressora, quantidade_vias, largura_papel="80"):

        nome_impressora = (self._validar_nome_impressora(nome_impressora))
        tipo_impressora = (self._normalizar_tipo_impressora(tipo_impressora))
        quantidade_vias = (self._normalizar_quantidade_vias(quantidade_vias))
        largura_papel = (self._normalizar_largura_papel(largura_papel))

        if tipo_impressora == "termica":
            largura_colunas = (32 if largura_papel == "58" else 48)
            separador = ("-" * largura_colunas)
            texto_base = (f"{'DUDÔCE'.center(largura_colunas)}\n{separador}\n{'TESTE DE IMPRESSÃO'.center(largura_colunas)}\n{'IMPRESSORA TÉRMICA'.center(largura_colunas)}\n{f'BOBINA {largura_papel} MM'.center(largura_colunas)}\n{separador}\nConfiguração realizada.\n")

        else:
            texto_base = ("DUDÔCE\n========================================\nTESTE DE IMPRESSÃO NORMAL\n========================================\nA impressora foi configurada corretamente.\n")

        for numero_via in range(1, quantidade_vias + 1):
            texto_teste = (f"{texto_base}\nVia {numero_via} de {quantidade_vias}\n\n\n")
            titulo_documento = (f"Teste Dudôce - Via {numero_via}")

            if tipo_impressora == "termica":
                self._imprimir_termica(nome_impressora=nome_impressora, texto=texto_teste, titulo_documento=(titulo_documento))

            else:
                self._imprimir_normal(nome_impressora=nome_impressora, texto=texto_teste, titulo_documento=(titulo_documento))

        return quantidade_vias

    def imprimir_pedido(self, pedido, configuracoes, tipo_copia="original"):

        if pedido is None:
            raise ValueError("Pedido não informado.")
        
        if not isinstance(configuracoes, dict):
            raise TypeError("As configurações de impressão devem ser um dicionário.")
        
        nome_impressora = (self._validar_nome_impressora(configuracoes.get("impressora", "")))
        tipo_impressora = (self._normalizar_tipo_impressora(configuracoes.get("tipo_impressora", "normal")))
        quantidade_vias = (self._normalizar_quantidade_vias(configuracoes.get("quantidade_vias", 1)))
        largura_papel = (self._normalizar_largura_papel(configuracoes.get("largura_papel", "80")))

        for numero_via in range(1, quantidade_vias + 1):
            if tipo_impressora == "termica":
                largura_colunas = (32 if largura_papel == "58" else 48)

            else:
                largura_colunas = 82
            texto_comprovante = (self.__comprovante_service.gerar_texto(pedido=pedido, largura_colunas=(largura_colunas), tipo_copia=tipo_copia, numero_via=numero_via, quantidade_vias=(quantidade_vias)))
            numero_pedido = (pedido.numero or "sem número")
            titulo_documento = (f"Pedido Dudôce #{numero_pedido}")

            if tipo_impressora == "termica":
                self._imprimir_termica(nome_impressora=(nome_impressora), texto=texto_comprovante, titulo_documento=(titulo_documento))
            
            else:
                self._imprimir_normal(nome_impressora=(nome_impressora), texto=texto_comprovante, titulo_documento=(titulo_documento))
        return quantidade_vias

    def _imprimir_termica(self, nome_impressora, texto, titulo_documento):
        
        impressora = None
        documento_iniciado = False
        pagina_iniciada = False

        try:
            impressora = (win32print.OpenPrinter(nome_impressora))
            documento = (titulo_documento, None, "RAW")
            win32print.StartDocPrinter(impressora, 1, documento)
            documento_iniciado = True
            win32print.StartPagePrinter(impressora)
            pagina_iniciada = True
            dados = (b"\x1b@" + texto.encode("cp850", errors="replace") + b"\n\n\n")
            bytes_enviados = (win32print.WritePrinter(impressora, dados))

            if (isinstance(bytes_enviados, int) and bytes_enviados != len(dados)):
                raise IOError("Nem todos os dados foram enviados à impressora.")
            
            win32print.EndPagePrinter(impressora)
            pagina_iniciada = False
            win32print.EndDocPrinter(impressora)
            documento_iniciado = False

        except Exception as erro:
            raise RuntimeError("Não foi possível imprimir na impressora térmica.") from erro
        
        finally:
            if impressora is not None:

                if pagina_iniciada:
                    try:
                        win32print.EndPagePrinter(impressora)
                    except Exception:
                        pass

                if documento_iniciado:
                    try:
                        win32print.EndDocPrinter(impressora)
                    except Exception:
                        pass
                try:
                    win32print.ClosePrinter(impressora)
                except Exception:
                    pass

    def _imprimir_normal(self, nome_impressora, texto, titulo_documento):

        contexto = None
        documento_iniciado = False

        try:
            contexto = win32ui.CreateDC()
            contexto.CreatePrinterDC(nome_impressora)
            dpi_x = contexto.GetDeviceCaps(win32con.LOGPIXELSX)
            dpi_y = contexto.GetDeviceCaps(win32con.LOGPIXELSY)
            largura_imprimivel = (contexto.GetDeviceCaps(win32con.HORZRES))
            altura_imprimivel = (contexto.GetDeviceCaps(win32con.VERTRES))
            margem_x = int(dpi_x * 0.4)
            margem_y = int(dpi_y * 0.4)
            altura_fonte = int(-10 * dpi_y / 72)
            fonte = win32ui.CreateFont({"name": "Courier New", "height": altura_fonte, "weight": 400})
            altura_linha = (abs(altura_fonte) + int(dpi_y * 0.04))
            limite_inferior = (altura_imprimivel - margem_y)
            contexto.StartDoc(titulo_documento)
            documento_iniciado = True
            contexto.StartPage()
            contexto.SelectObject(fonte)
            posicao_y = margem_y

            for linha in texto.splitlines():
                if (posicao_y + altura_linha > limite_inferior):
                    contexto.EndPage()
                    contexto.StartPage()
                    contexto.SelectObject(fonte)
                    posicao_y = margem_y
                linha = str(linha)
                contexto.TextOut(margem_x, posicao_y, linha)
                posicao_y += altura_linha
            contexto.EndPage()
            contexto.EndDoc()
            documento_iniciado = False

        except Exception as erro:
            if (contexto is not None and documento_iniciado):
                try:
                    contexto.AbortDoc()
                except Exception:
                    pass
            raise RuntimeError("Não foi possível imprimir na impressora normal.") from erro
        finally:
            if contexto is not None:
                try:
                    contexto.DeleteDC()
                except Exception:
                    pass