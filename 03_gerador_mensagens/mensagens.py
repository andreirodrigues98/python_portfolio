import datetime
from pathlib import Path

historico = []

def salvar_txt(mensagem):
    salvar_msg = input('Deseja salvar a msg em formato txt? [s/n]: ').strip().lower()

    if salvar_msg in ['n', 'não', 'nao']:
        return

    if salvar_msg in ['sim', 's']:
        caminho = input('Informe o nome do arquivo .txt: ').strip()

        if not caminho:
            print('Preencha o campo corretamente.')
            return

        if not caminho.lower().endswith('.txt'):
            caminho += '.txt'

        arquivo_txt = Path(caminho)

        with open(arquivo_txt, 'w', encoding='utf-8') as arquivo:
            arquivo.write(mensagem)

        print('Mensagem salva com sucesso!')
    else:
        print('Opção inválida.')
        return

def adicionar_historico(historico, tipo, cliente, mensagem):
    registro = {
        "tipo": tipo,
        "cliente": cliente,
        "mensagem": mensagem,
        "data_hora": datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    }

    historico.append(registro)

def listar_historico(historico):
    print('\n========== HISTÓRICO DE MENSAGENS ==========')

    if not historico:
        print('Nenhuma mensagem foi gerada ainda.')
        return

    for indice, registro in enumerate(historico, start=1):
        print(f'\nMensagem {indice}:')
        print(f'Tipo: {registro["tipo"]}')
        print(f'Cliente: {registro["cliente"]}')
        print(f'Data/Hora: {registro["data_hora"]}')
        print('\nMensagem:')
        print(registro["mensagem"])

def obter_modelos():
    modelos = {
        "cobranca": """
{saudacao}, {nome}. Tudo bem?

Estou entrando em contato para lembrar sobre o pagamento
no valor de R$ {valor:.2f}, com vencimento em {vencimento}.

Qualquer dúvida, estou à disposição. Tenha {periodo}!
""",

        "orcamento": """
{saudacao}, {nome}. Tudo bem?

Segue o orçamento de {produto}, conforme solicitado.

Descrição: {descricao}
Valor: R$ {valor:.2f}
Prazo estimado: {prazo}

Qualquer dúvida, estou à disposição. Tenha {periodo}!
""",

        "agendamento": """
{saudacao}, {nome}. Tudo bem?

Estou entrando em contato para confirmar seu agendamento.

Data: {data}
Horário: {horario}
Local/Forma de atendimento: {local}

Qualquer dúvida, estou à disposição. Tenha {periodo}!
"""
    }

    return modelos

def obter_saudacao():
    agora = datetime.datetime.now()

    if agora.hour < 12:
        saudacao = 'Bom dia'
        periodo = 'um ótimo dia'
    elif agora.hour < 18:
        saudacao = 'Boa tarde'
        periodo = 'uma ótima tarde'
    else:
        saudacao = 'Boa noite'
        periodo = 'uma ótima noite'

    return saudacao, periodo

def gerar_mensagem_cobranca(historico):
    nome = input('\nInforme o nome do cliente: ').strip()

    if not nome:
        print('Preencha o campo corretamente.')
        return

    try:
        valor_cobranca = float(input('Digite o valor de cobrança: ').strip())

        if valor_cobranca <= 0:
            print('O valor tem que ser maior que 0.')
            return
    except ValueError:
        print('Preencha o campo corretamente, deve ser um inteiro ou decimal.')
        return

    data_vencimento = input('Digite a data de vencimento(dd/mm): ').strip()

    if not data_vencimento:
        print('Preencha o campo corretamente.')
        return

    saudacao, periodo = obter_saudacao()

    modelos = obter_modelos()
    modelo = modelos["cobranca"]

    mensagem = modelo.format(
        saudacao=saudacao,
        nome=nome,
        valor=valor_cobranca,
        vencimento=data_vencimento,
        periodo=periodo
    )

    print(mensagem)

    adicionar_historico(historico, 'Cobrança', nome, mensagem)
    salvar_txt(mensagem)

def gerar_mensagem_orcamento(historico):
    nome = input('\nDigite o nome do cliente: ').strip()

    if not nome:
        print('Preencha o campo corretamente.')
        return

    nome_produto = input('Digite o nome do Produto/Serviço: ').strip()

    if not nome_produto:
        print('Preencha o campo corretamente.')
        return

    descricao = input(f'Digite a descrição do {nome_produto}: ').strip()

    if not descricao:
        print('Preencha o campo corretamente.')
        return

    try:
        valor = float(input(f'Digite o valor do {nome_produto}: ').strip())

        if valor <= 0:
            print('O valor deve ser maior que 0')
            return
    except ValueError:
        print('O valor deve ser um numero inteiro ou decimal.')
        return

    prazo = input('Informe o prazo estimado: ').strip()

    if not prazo:
        print('Preencha o campo corretamente.')
        return

    saudacao, periodo = obter_saudacao()

    modelos = obter_modelos()
    modelo = modelos["orcamento"]

    mensagem = modelo.format(
        saudacao=saudacao,
        nome=nome,
        produto=nome_produto,
        descricao=descricao,
        valor=valor,
        prazo=prazo,
        periodo=periodo
    )

    print(mensagem)

    adicionar_historico(historico, 'Orçamento', nome, mensagem)
    salvar_txt(mensagem)

def gerar_mensagem_agendamento(historico):
    nome = input('\nDigite o nome do cliente: ').strip()

    if not nome:
        print('Preencha o campo corretamente.')
        return

    try:
        dia = int(input('Informe o dia do agendamento(ex: 15): ').strip())

        if dia < 1 or dia > 31:
            print('Digite um numero de 1 a 31.')
            return
    except ValueError:
        print('Digite um numero inteiro de 1 a 31.')
        return

    try:
        mes = int(input('Informe o mes do agendamento(ex: 12): ').strip())

        if mes < 1 or mes > 12:
            print('Digite um numero de 1 a 12.')
            return
    except ValueError:
        print('Digite um numero inteiro de 1 a 12.')
        return

    data = f'{dia:02d}/{mes:02d}'

    horario = input('Informe o horário do agendamente (ex: 15:00): ').strip()

    if not horario:
        print('Preencha o campo corretamente.')
        return

    local = input('Informe o local da consulta(Presencial/Online): ').strip()

    if not local:
        print('Preencha o campo corretamente.')
        return

    saudacao, periodo = obter_saudacao()

    modelos = obter_modelos()
    modelo = modelos["agendamento"]

    mensagem = modelo.format(
        saudacao=saudacao,
        nome=nome,
        data=data,
        horario=horario,
        local=local,
        periodo=periodo
    )

    print(mensagem)

    adicionar_historico(historico, 'Agendamento', nome, mensagem)
    salvar_txt(mensagem)

def menu():
    print('========== MENU ==========')
    print('1 - Mensagem Cobrança')
    print('2 - Mensagem Orçamento')
    print('3 - Mensagem Agendamento')
    print('4 - Ver Histórico')
    print('0 - Sair')

def main():
    while True:
        menu()

        try:
            opcao = int(input('\nInforme uma opção acima: ').strip())

            if opcao < 0 or opcao > 4:
                print('Digite um numero de 0 a 4.')
                continue
        except ValueError:
            print('Digite um numero de 0 a 4.')
            continue

        if opcao == 1:
            print('=========== MENSAGEM COBRANÇA ==========')
            gerar_mensagem_cobranca(historico)

        elif opcao == 2:
            print('=========== MENSAGEM ORÇAMENTO ==========')
            gerar_mensagem_orcamento(historico)

        elif opcao == 3:
            print('=========== MENSAGEM AGENDAMENTO ==========')
            gerar_mensagem_agendamento(historico)

        elif opcao == 4:
            listar_historico(historico)

        elif opcao == 0:
            print('Finalizando o sistema...')
            break

        else:
            print('Opção invalida, digite uma opção valida.')
            continue

if __name__ == '__main__':
    main()