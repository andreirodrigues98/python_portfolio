from datetime import datetime

class RelatorioService:

    def _filtrar_pedidos_por_data(self, pedidos, data_escolhida):

        pedidos_filtrados = []

        for pedido in pedidos:
            
            if pedido.data_pedido == data_escolhida:
                pedidos_filtrados.append(pedido)

        return pedidos_filtrados
    
    def _calcular_valor_total(self, pedidos):

        valor_total = 0.0

        for pedido in pedidos:
            try:
                total_pedido = float( pedido.total)

            except (TypeError, ValueError):
                total_pedido = 0.0

            valor_total += total_pedido

        return valor_total
    
    def _calcular_detalhes_do_periodo(self, pedidos_filtrados):

        if not pedidos_filtrados:

            return {
                "maior_pedido": None,
                "menor_pedido": None,
                "horario_mais_pedidos": None,
                "quantidade_horario_mais_pedidos": 0
            }

        maior_pedido = pedidos_filtrados[0]
        menor_pedido = pedidos_filtrados[0]

        contagem_horarios = {}

        for pedido in pedidos_filtrados:

            if pedido.total > maior_pedido.total:
                maior_pedido = pedido

            if pedido.total < menor_pedido.total:
                menor_pedido = pedido

            if not pedido.horario:
                continue

            try:
                hora = pedido.horario.split(":")[0]

            except (AttributeError, IndexError):
                continue

            if hora not in contagem_horarios:
                contagem_horarios[hora] = 0

            contagem_horarios[hora] += 1

        horario_mais_pedidos = None
        maior_quantidade_horario = 0

        for hora, quantidade in contagem_horarios.items():

            if quantidade > maior_quantidade_horario:

                maior_quantidade_horario = quantidade
                horario_mais_pedidos = hora

        return {
            "maior_pedido": maior_pedido,
            "menor_pedido": menor_pedido,
            "horario_mais_pedidos": horario_mais_pedidos,
            "quantidade_horario_mais_pedidos": maior_quantidade_horario
        }

    def _contar_impressos(self, pedidos):

        quantidade_impressos = 0

        for pedido in pedidos:

            if pedido.foi_impresso:
                quantidade_impressos += 1
        
        return quantidade_impressos
    
    def gerar_relatorio_diario(self, pedidos,data_escolhida):

        periodo = str(data_escolhida or "").strip()

        formato_valido = (len(periodo) == 10 and periodo[2] == "/" and periodo[5] == "/")

        if not formato_valido:
            raise ValueError("Informe o período diário ""no formato DD/MM/AAAA.")

        try:
            data_validada = datetime.strptime(periodo, "%d/%m/%Y")

        except ValueError:
            raise ValueError("Informe uma data diária válida ""no formato DD/MM/AAAA." )

        periodo_normalizado = ( data_validada.strftime("%d/%m/%Y"))

        pedidos_do_dia = (self._filtrar_pedidos_por_data(pedidos, periodo_normalizado))

        return self._montar_resultado(pedidos_filtrados=pedidos_do_dia, periodo=periodo_normalizado)

    def _filtrar_pedidos_por_mes(self, pedidos, mes_escolhido, ano_escolhido):

        pedidos_do_mes = []

        for pedido in pedidos:
            if not pedido.data_pedido:
                continue

            try:
                data_pedido = datetime.strptime(pedido.data_pedido, "%d/%m/%Y")

            except (TypeError, ValueError):
                continue

            if (data_pedido.strftime("%m") == mes_escolhido and data_pedido.strftime("%Y") == ano_escolhido):
                
                pedidos_do_mes.append(pedido)

        return pedidos_do_mes

    def gerar_relatorio_mensal(self,  pedidos, periodo):

        periodo = str(periodo or "").strip()

        formato_valido = (len(periodo) == 7 and periodo[2] == "/" )

        if not formato_valido:
            raise ValueError( "Informe o período mensal ""no formato MM/AAAA.")

        try:
            data_validada = datetime.strptime(periodo, "%m/%Y")

        except ValueError:
            raise ValueError("Informe um mês válido ""no formato MM/AAAA.")

        mes_escolhido = (data_validada.strftime("%m") )
        ano_escolhido = ( data_validada.strftime("%Y") )

        periodo_normalizado = ( f"{mes_escolhido}/"f"{ano_escolhido}")

        pedidos_do_mes = (self._filtrar_pedidos_por_mes(pedidos,mes_escolhido,ano_escolhido ))

        return self._montar_resultado(pedidos_filtrados=pedidos_do_mes, periodo=periodo_normalizado)

    def _filtrar_pedidos_por_ano(self, pedidos, ano_escolhido):

        pedidos_do_ano = []

        for pedido in pedidos:

            if not pedido.data_pedido:
                continue

            try:
                data_pedido = datetime.strptime(pedido.data_pedido, "%d/%m/%Y" )

            except (TypeError, ValueError):
                continue

            if (data_pedido.strftime("%Y") == ano_escolhido):

                pedidos_do_ano.append( pedido)

        return pedidos_do_ano

    def gerar_relatorio_anual(self, pedidos,  periodo):

        ano_escolhido = str(periodo or "").strip()

        if (len(ano_escolhido) != 4 or not ano_escolhido.isdigit()):
            raise ValueError("Informe o período anual " "no formato AAAA.")

        try:
            datetime.strptime(ano_escolhido, "%Y")

        except ValueError:
            raise ValueError( "Informe um ano válido " "no formato AAAA." )

        pedidos_do_ano = (self._filtrar_pedidos_por_ano(pedidos, ano_escolhido ))

        return self._montar_resultado( pedidos_filtrados=pedidos_do_ano, periodo=ano_escolhido )

    def _montar_resultado(self, pedidos_filtrados, periodo):

        pedidos_ordenados = sorted(pedidos_filtrados, key=self._chave_ordenacao_pedido, reverse=True)
        quantidade_pedidos = len(pedidos_ordenados)

        valor_total = ( self._calcular_valor_total(pedidos_ordenados))
        quantidade_impressos = (self._contar_impressos(pedidos_ordenados) )
        quantidade_nao_impressos = (quantidade_pedidos - quantidade_impressos)

        if quantidade_pedidos > 0:
            ticket_medio = (valor_total / quantidade_pedidos)

        else:
            ticket_medio = 0.0

        detalhes = (self._calcular_detalhes_do_periodo(pedidos_ordenados))

        produtos = (self._calcular_produtos_vendidos(pedidos_ordenados))

        return {
            "periodo": periodo,
            "quantidade_pedidos": quantidade_pedidos,
            "valor_total": valor_total,
            "ticket_medio": ticket_medio,
            "quantidade_impressos": quantidade_impressos,
            "quantidade_nao_impressos": quantidade_nao_impressos,
            "pedidos": pedidos_ordenados,
            **detalhes,
            **produtos
        }

    @staticmethod
    def _chave_ordenacao_pedido(pedido):

        data_pedido = (pedido.data_pedido or "")

        horario_pedido = (pedido.horario or "00:00")

        try:
            return datetime.strptime((f"{data_pedido} " f"{horario_pedido}"), "%d/%m/%Y %H:%M")

        except (TypeError, ValueError):
            return datetime.min

    def _calcular_produtos_vendidos(self, pedidos_filtrados):

        produtos_agrupados = {}

        for pedido in pedidos_filtrados:

            itens_dados = getattr(pedido, "itens_dados", [])

            if not isinstance(itens_dados, list):
                continue

            for item in itens_dados:
                
                if not isinstance(item, dict):
                    continue

                nome_produto = str(item.get("nome", "Produto sem nome" ) or "Produto sem nome").strip()
                quantidade_produto = item.get("quantidade",  0)

                try:
                    quantidade_produto = int( quantidade_produto)

                except (TypeError, ValueError):
                    quantidade_produto = 0

                if quantidade_produto <= 0:
                    continue

                chave_produto = (nome_produto.casefold())

                if chave_produto not in produtos_agrupados:
                    produtos_agrupados[chave_produto] = {"nome": nome_produto, "quantidade": 0 }

                produtos_agrupados[chave_produto]["quantidade"] += (quantidade_produto)

        produtos_vendidos = sorted(produtos_agrupados.values(), key=lambda produto: (produto["nome"].casefold()))
        ranking_ordenado = sorted(produtos_agrupados.values(), key=lambda produto: (-produto["quantidade"], produto["nome"].casefold()))

        ranking_produtos = []

        quantidade_anterior = None
        posicao_atual = 0

        for indice, produto in enumerate(ranking_ordenado, start=1):
            if (produto["quantidade"] != quantidade_anterior ):
                posicao_atual = indice
                quantidade_anterior = (produto["quantidade"])

            produto_ranking = dict(produto)

            produto_ranking["posicao"] = posicao_atual

            ranking_produtos.append(produto_ranking)

        quantidade_total_produtos = sum(produto["quantidade"] for produto in produtos_agrupados.values())

        return {
            "produtos_vendidos": produtos_vendidos,
            "ranking_produtos": ranking_produtos,
            "quantidade_total_produtos": quantidade_total_produtos,
            "quantidade_produtos_distintos": len(produtos_agrupados)
        }





