# OrderFlow Desktop

Sistema desktop para gerenciamento de pedidos, impressão de comprovantes e acompanhamento de vendas.

O projeto foi desenvolvido em Python com interface gráfica utilizando CustomTkinter e integração com Firebase/Firestore.

## Funcionalidades

- Recebimento de pedidos em tempo real
- Listagem de pedidos pendentes
- Histórico de pedidos
- Reimpressão de pedidos
- Impressão em impressoras comuns e térmicas
- Compatibilidade com bobinas de 58 mm e 80 mm
- Configuração da impressora
- Aviso sonoro para novos pedidos
- Relatórios diários, mensais e anuais
- Geração de executável para Windows
- Instalador para distribuição do sistema

## Tecnologias utilizadas

- Python
- CustomTkinter
- Firebase Admin SDK
- Firestore
- PyWin32
- Pillow
- PyInstaller
- Inno Setup

## Estrutura do projeto


saas_lanchonete/
├── recursos/
│   ├── icones/
│   └── sons/
│
├── src/
│   ├── controladores/
│   ├── modelos/
│   ├── servicos/
│   ├── ui/
│   └── main.py
│
├── .gitignore
├── README.md
└── requirements.txt
