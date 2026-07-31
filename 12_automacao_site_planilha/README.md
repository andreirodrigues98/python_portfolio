Automação de Cadastros com Python

Projeto desenvolvido para automatizar o preenchimento de formulários web utilizando dados armazenados em uma planilha Excel.

A aplicação lê os cadastros da planilha, valida os campos obrigatórios, abre o site no navegador, realiza o login uma única vez e adiciona todos os registros válidos na mesma página.

Ao final, o programa gera uma nova planilha com o resultado da automação e os cadastros inválidos.

Funcionalidades

Leitura de dados de uma planilha .xlsx;

Conversão das linhas da planilha em dicionários Python;

Validação dos campos obrigatórios;

Separação entre cadastros válidos e inválidos;

Abertura automática do site no navegador;

Login automático;

Preenchimento do formulário com PyAutoGUI;

Suporte a textos com acentos usando Pyperclip;

Seleção do estado no formulário;

Cadastro de vários registros na mesma página;

Tratamento de erros durante a automação;

Geração de relatório Excel com cadastros processados, status, mensagens e registros inválidos.

Tecnologias utilizadas

Python

OpenPyXL

PyAutoGUI

Pyperclip

Pathlib

Webbrowser

Estrutura do projeto

12_automacao_site_planilha_python_portfolio/
│
├── main.py
├── planilha.py
├── automacao.py
├── cadastros_teste_automacao.xlsx
├── relatorio_automacao.xlsx
├── imagens/
│   ├── entrar.png
│   └── add.png
└── README.md

Responsabilidade dos arquivos

main.py

Coordena o fluxo principal da aplicação:

carrega os cadastros;

valida os dados;

separa registros válidos e inválidos;

abre o site;

realiza o login;

executa a automação;

registra os resultados;

solicita a geração do relatório.

planilha.py

Responsável pelas operações relacionadas ao Excel:

leitura da planilha;

transformação das linhas em dicionários;

validação dos campos obrigatórios;

criação do relatório final.

automacao.py

Responsável pela interação com o navegador:

abertura do site;

preenchimento do login;

preenchimento do formulário;

seleção do estado;

clique no botão de cadastro;

retorno ao início da página.

Formato da planilha de entrada

A planilha deve possuir uma aba chamada Cadastros com as seguintes colunas:

Nome

E-mail

Telefone

Empresa

Cargo

Cidade

Estado

Observações

Os campos obrigatórios são:

nome;

e-mail;

telefone;

empresa;

cargo;

cidade;

estado.

O campo observações é opcional.

Instalação

Crie um ambiente virtual:

python -m venv venv

Ative o ambiente virtual no Windows:

venv\Scripts\activate

Instale as dependências:

pip install openpyxl pyautogui pyperclip opencv-python

Como executar

Coloque a planilha de entrada na pasta do projeto.

Confira se a aba se chama Cadastros.

Ajuste no main.py:

URL do site;

e-mail de login;

senha;

nome do arquivo Excel.

Ajuste as coordenadas utilizadas em automacao.py, caso necessário.

Execute:

python main.py

Fluxo da aplicação

Planilha Excel
      ↓
Leitura dos cadastros
      ↓
Validação dos campos
      ↓
Separação entre válidos e inválidos
      ↓
Abertura do site
      ↓
Login automático
      ↓
Preenchimento dos cadastros válidos
      ↓
Registro dos resultados
      ↓
Geração do relatório Excel

Relatório gerado

O arquivo relatorio_automacao.xlsx possui duas abas.

Resultados

Nome

Status

Mensagem

Ana Silva

Sucesso

Cadastro realizado

Inválidos

Nome

E-mail

Telefone

Empresa

Cargo

Cidade

Estado

Erro

Observações importantes

O PyAutoGUI controla o mouse e o teclado com base na posição dos elementos na tela.

Por isso, a automação pode ser afetada por:

resolução do monitor;

zoom do navegador;

posição da janela;

velocidade de carregamento da página;

mudanças no layout do site.

Durante a execução, não utilize o mouse ou o teclado.

O recurso FAILSAFE está habilitado. Para interromper a automação, mova rapidamente o mouse para o canto superior esquerdo da tela.

Aprendizados aplicados

Este projeto trabalha conceitos importantes de Python:

funções;

módulos;

listas;

dicionários;

loops;

condicionais;

tratamento de exceções;

leitura e escrita de arquivos;

validação de dados;

separação de responsabilidades;

automação de tarefas;

integração entre planilhas e navegador.

Possíveis melhorias futuras

substituir coordenadas fixas por reconhecimento de imagens em todos os campos;

gerar logs em arquivo;

criar uma interface gráfica;

permitir a seleção da planilha pelo usuário;

adicionar contador de progresso;

criar arquivo de configuração;

utilizar Selenium ou Playwright para uma automação menos dependente da tela.

Autor

Desenvolvido por Andrei Rodrigues.
