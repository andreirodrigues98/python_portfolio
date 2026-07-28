from textwrap import wrap

class ComprovanteService:

    TIPOS_COPIA = {"original": "IMPRESSÃO ORIGINAL", "reimpressao": "REIMPRESSÃO", "historico": "CÓPIA DO HISTÓRICO" }

    @staticmethod
    def _formatar_moeda(valor):

        try:
            valor = float(valor)

        except (TypeError, ValueError):
            valor = 0

        valor_formatado = (f"{valor:,.2f}".replace(",", "TEMP").replace(".", ",").replace("TEMP", "."))

        return f"R$ {valor_formatado}"

    @staticmethod
    def _normalizar_texto(valor, valor_padrao=""):

        if valor is None:
            return valor_padrao

        texto = str(valor).strip()

        if not texto:
            return valor_padrao

        return texto

    @staticmethod
    def _centralizar(texto, largura):

        texto = str(texto)

        if len(texto) > largura:
            texto = texto[:largura]

        return texto.center(largura)

    @staticmethod
    def _quebrar_texto(texto, largura, indentacao=""):

        texto = str(texto or "")

        partes = texto.splitlines()

        if not partes:
            return [""]

        resultado = []

        for parte in partes:
            parte = parte.strip()

            if not parte:
                resultado.append("")
                continue

            linhas_quebradas = wrap(parte, width=largura, replace_whitespace=False, drop_whitespace=True, break_long_words=True, break_on_hyphens=False, subsequent_indent=indentacao)

            if linhas_quebradas:
                resultado.extend(linhas_quebradas)

            else:
                resultado.append("")

        return resultado

    def _adicionar_campo(self, linhas, titulo, valor, largura, valor_padrao="Não informado"):

        valor = self._normalizar_texto(valor, valor_padrao)

        texto = f"{titulo}: {valor}"

        linhas.extend(self._quebrar_texto(texto, largura, indentacao=" " * ( len(titulo) + 2)))

    def gerar_texto(self, pedido, largura_colunas=48, tipo_copia="original", numero_via=1, quantidade_vias=1):

        if pedido is None:
            raise ValueError("Pedido não informado.")

        try:
            largura_colunas = int(largura_colunas)

        except (TypeError, ValueError):
            largura_colunas = 48

        if largura_colunas < 24:
            largura_colunas = 24

        try:
            numero_via = int(numero_via)

        except (TypeError, ValueError):
            numero_via = 1

        try:
            quantidade_vias = int(quantidade_vias)

        except (TypeError, ValueError):
            quantidade_vias = 1

        numero_via = max(numero_via, 1)

        quantidade_vias = max(quantidade_vias, 1)

        tipo_copia = str(tipo_copia or "original").strip().lower()

        texto_tipo_copia = (self.TIPOS_COPIA.get(tipo_copia,self.TIPOS_COPIA["original"]))

        separador = ("-" * largura_colunas)

        linhas = [self._centralizar("DUDÔCE", largura_colunas), self._centralizar("PEDIDO PARA PRODUÇÃO",largura_colunas), self._centralizar("COMPROVANTE NÃO FISCAL",largura_colunas), separador]

        numero_pedido = ( self._normalizar_texto(pedido.numero,"Não informado"))

        codigo_pedido = (self._normalizar_texto(pedido.codigo_pedido, ""))

        self._adicionar_campo(linhas=linhas, titulo="Pedido", valor=f"#{numero_pedido}", largura=largura_colunas)

        if codigo_pedido: self._adicionar_campo(linhas=linhas, titulo="Código", valor=codigo_pedido, largura=largura_colunas)

        data_pedido = (self._normalizar_texto(pedido.data_pedido, "Data não informada"))

        horario_pedido = (self._normalizar_texto(pedido.horario, "Horário não informado"))

        self._adicionar_campo(linhas=linhas, titulo="Data", valor=data_pedido, largura=largura_colunas)

        self._adicionar_campo(linhas=linhas,  titulo="Horário", valor=horario_pedido, largura=largura_colunas)

        linhas.append(separador)

        self._adicionar_campo(linhas=linhas, titulo="Cliente", valor=pedido.nome_cliente, largura=largura_colunas, valor_padrao="Cliente não informado")

        self._adicionar_campo(linhas=linhas, titulo="WhatsApp", valor=pedido.whatsapp, largura=largura_colunas, valor_padrao="Não informado")

        linhas.extend([separador, "ITENS DO PEDIDO"])

        itens = pedido.itens

        if not isinstance(itens,  list):
            itens = []

        if not itens:
            linhas.append("Nenhum item informado.")

        else:
            for indice, item in enumerate(itens, start=1):

                texto_item = (self._normalizar_texto(item, "Item não informado"))

                partes_item = (texto_item.splitlines())

                for indice_parte, parte in enumerate(partes_item):
                    parte = parte.strip()

                    if not parte:
                        continue

                    if indice_parte == 0:
                        prefixo = (f"{indice}. " )

                    else:
                        prefixo = "   "

                    texto_linha = (f"{prefixo}{parte}")

                    linhas.extend(self._quebrar_texto(texto_linha, largura_colunas, indentacao=" " * len(prefixo)))

                if indice < len(itens):
                    linhas.append("")

        linhas.append(separador)

        total_formatado = (self._formatar_moeda(pedido.total))
        linhas.extend(self._quebrar_texto(f"TOTAL: {total_formatado}", largura_colunas))

        linhas.append(separador)

        observacao = (self._normalizar_texto(pedido.observacao, "Nenhuma observação."))

        linhas.append("OBSERVAÇÃO")

        linhas.extend(self._quebrar_texto(observacao, largura_colunas))

        linhas.extend([separador,self._centralizar( texto_tipo_copia, largura_colunas),self._centralizar((f"VIA {numero_via} " f"DE {quantidade_vias}" ),largura_colunas),separador, self._centralizar("SEM VALOR FISCAL", largura_colunas), "", "", ""])

        return "\n".join(linhas)