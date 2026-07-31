const telaLogin = document.getElementById("tela-login");
const telaPrincipal = document.getElementById("tela-principal");
const formLogin = document.getElementById("form-login");
const campoUsuario = document.getElementById("usuario");
const campoSenha = document.getElementById("senha");
const mostrarSenha = document.getElementById("mostrar-senha");
const lembrarUsuario = document.getElementById("lembrar-usuario");
const nomeUsuario = document.getElementById("nome-usuario");
const botaoSair = document.getElementById("botao-sair");

const formCadastro = document.getElementById("form-cadastro");
const botaoLimparFormulario = document.getElementById("botao-limpar-formulario");
const botaoLimparLista = document.getElementById("botao-limpar-lista");
const botaoIniciar = document.getElementById("botao-iniciar");
const botaoExportar = document.getElementById("botao-exportar");
const corpoTabela = document.getElementById("corpo-tabela");
const mensagemCadastro = document.getElementById("mensagem-cadastro");

const modalVisualizar = document.getElementById("modal-visualizar");
const fecharModal = document.getElementById("fechar-modal");
const dadosVisualizacao = document.getElementById("dados-visualizacao");

let cadastros = [];
let proximoId = 1;
let idEmEdicao = null;

const usuarioSalvo = localStorage.getItem("usuarioLembrado");

if (usuarioSalvo) {
    campoUsuario.value = usuarioSalvo;
    lembrarUsuario.checked = true;
}

mostrarSenha.addEventListener("click", function () {
    const senhaEstaEscondida = campoSenha.type === "password";
    campoSenha.type = senhaEstaEscondida ? "text" : "password";
    mostrarSenha.textContent = senhaEstaEscondida ? "Esconder" : "Mostrar";
});

formLogin.addEventListener("submit", function (evento) {
    evento.preventDefault();

    const usuarioDigitado = campoUsuario.value.trim();
    const senhaDigitada = campoSenha.value.trim();

    if (!usuarioDigitado || !senhaDigitada) {
        document.getElementById("mensagem-login").textContent =
            "Preencha o usuário e a senha.";
        return;
    }

    if (lembrarUsuario.checked) {
        localStorage.setItem("usuarioLembrado", usuarioDigitado);
    } else {
        localStorage.removeItem("usuarioLembrado");
    }

    nomeUsuario.textContent = usuarioDigitado;
    document.getElementById("mensagem-login").textContent = "";
    telaLogin.classList.add("escondida");
    telaPrincipal.classList.remove("escondida");
});

botaoSair.addEventListener("click", function () {
    campoSenha.value = "";
    telaPrincipal.classList.add("escondida");
    telaLogin.classList.remove("escondida");
});

formCadastro.addEventListener("submit", function (evento) {
    evento.preventDefault();

    const cadastro = obterDadosFormulario();

    if (idEmEdicao !== null) {
        const indice = cadastros.findIndex(item => item.id === idEmEdicao);

        if (indice !== -1) {
            cadastro.id = idEmEdicao;
            cadastro.status = cadastros[indice].status;
            cadastro.mensagem = cadastros[indice].mensagem;
            cadastros[indice] = cadastro;
        }

        mensagemCadastro.textContent = "Cadastro atualizado com sucesso.";
        idEmEdicao = null;
    } else {
        cadastro.id = proximoId;
        cadastro.status = "Pendente";
        cadastro.mensagem = "Aguardando envio";
        cadastros.push(cadastro);
        proximoId++;

        mensagemCadastro.textContent = "Cadastro adicionado com sucesso.";
    }

    formCadastro.reset();
    atualizarTabela();
});

botaoLimparFormulario.addEventListener("click", function () {
    formCadastro.reset();
    idEmEdicao = null;
    mensagemCadastro.textContent = "";
});

botaoLimparLista.addEventListener("click", function () {
    cadastros = cadastros.filter(cadastro => cadastro.status === "Enviado");
    atualizarTabela();
});

botaoIniciar.addEventListener("click", async function () {
    const pendentes = cadastros.filter(cadastro => cadastro.status === "Pendente");

    if (pendentes.length === 0) {
        alert("Não existem cadastros pendentes.");
        return;
    }

    botaoIniciar.disabled = true;
    botaoIniciar.textContent = "Automação em andamento...";

    for (const cadastro of pendentes) {
        cadastro.status = "Enviando";
        cadastro.mensagem = "Processando cadastro";
        atualizarTabela();

        await esperar(700);

        const ocorreuErro = Math.random() < 0.2;

        if (ocorreuErro) {
            cadastro.status = "Erro";
            cadastro.mensagem = "Erro simulado durante o envio";
        } else {
            cadastro.status = "Enviado";
            cadastro.mensagem = "Cadastro concluído";
        }

        atualizarTabela();
    }

    botaoIniciar.disabled = false;
    botaoIniciar.textContent = "Iniciar automação";
    alert("Automação simulada finalizada.");
});

botaoExportar.addEventListener("click", function () {
    if (cadastros.length === 0) {
        alert("Não existem cadastros para exportar.");
        return;
    }

    const cabecalho = [
        "ID",
        "Nome",
        "E-mail",
        "Telefone",
        "Empresa",
        "Cargo",
        "Cidade",
        "Estado",
        "Status",
        "Mensagem"
    ];

    const linhas = cadastros.map(cadastro => [
        cadastro.id,
        cadastro.nome,
        cadastro.email,
        cadastro.telefone,
        cadastro.empresa,
        cadastro.cargo,
        cadastro.cidade,
        cadastro.estado,
        cadastro.status,
        cadastro.mensagem
    ]);

    const conteudoCSV = [cabecalho, ...linhas]
        .map(linha => linha.map(valor => `"${String(valor).replaceAll('"', '""')}"`).join(";"))
        .join("\n");

    const arquivo = new Blob(["\uFEFF" + conteudoCSV], {
        type: "text/csv;charset=utf-8;"
    });

    const link = document.createElement("a");
    link.href = URL.createObjectURL(arquivo);
    link.download = "relatorio_cadastros.csv";
    link.click();

    URL.revokeObjectURL(link.href);
});

fecharModal.addEventListener("click", function () {
    modalVisualizar.classList.add("escondida");
});

modalVisualizar.addEventListener("click", function (evento) {
    if (evento.target === modalVisualizar) {
        modalVisualizar.classList.add("escondida");
    }
});

function obterDadosFormulario() {
    return {
        nome: document.getElementById("nome").value.trim(),
        email: document.getElementById("email").value.trim(),
        telefone: document.getElementById("telefone").value.trim(),
        empresa: document.getElementById("empresa").value.trim(),
        cargo: document.getElementById("cargo").value.trim(),
        cidade: document.getElementById("cidade").value.trim(),
        estado: document.getElementById("estado").value,
        observacoes: document.getElementById("observacoes").value.trim()
    };
}

function atualizarTabela() {
    corpoTabela.innerHTML = "";

    if (cadastros.length === 0) {
        corpoTabela.innerHTML = `
            <tr>
                <td colspan="7" class="sem-registros">
                    Nenhum cadastro adicionado.
                </td>
            </tr>
        `;
    } else {
        cadastros.forEach(cadastro => {
            const linha = document.createElement("tr");

            linha.innerHTML = `
                <td>${cadastro.id}</td>
                <td>${escaparHTML(cadastro.nome)}</td>
                <td>${escaparHTML(cadastro.email)}</td>
                <td>${escaparHTML(cadastro.telefone)}</td>
                <td>${escaparHTML(cadastro.empresa)}</td>
                <td>
                    <span class="status ${classeStatus(cadastro.status)}">
                        ${cadastro.status}
                    </span>
                </td>
                <td>
                    <div class="acoes-tabela">
                        <button class="botao secundario" onclick="visualizarCadastro(${cadastro.id})">
                            Visualizar
                        </button>
                        <button class="botao principal" onclick="editarCadastro(${cadastro.id})">
                            Editar
                        </button>
                        <button class="botao perigo" onclick="excluirCadastro(${cadastro.id})">
                            Excluir
                        </button>
                    </div>
                </td>
            `;

            corpoTabela.appendChild(linha);
        });
    }

    atualizarResumo();
}

function atualizarResumo() {
    document.getElementById("total-cadastros").textContent = cadastros.length;
    document.getElementById("total-pendentes").textContent =
        cadastros.filter(item => item.status === "Pendente").length;
    document.getElementById("total-enviados").textContent =
        cadastros.filter(item => item.status === "Enviado").length;
    document.getElementById("total-erros").textContent =
        cadastros.filter(item => item.status === "Erro").length;
}

function classeStatus(status) {
    const classes = {
        Pendente: "status-pendente",
        Enviando: "status-enviando",
        Enviado: "status-enviado",
        Erro: "status-erro"
    };

    return classes[status] || "status-pendente";
}

function editarCadastro(id) {
    const cadastro = cadastros.find(item => item.id === id);

    if (!cadastro) {
        return;
    }

    document.getElementById("nome").value = cadastro.nome;
    document.getElementById("email").value = cadastro.email;
    document.getElementById("telefone").value = cadastro.telefone;
    document.getElementById("empresa").value = cadastro.empresa;
    document.getElementById("cargo").value = cadastro.cargo;
    document.getElementById("cidade").value = cadastro.cidade;
    document.getElementById("estado").value = cadastro.estado;
    document.getElementById("observacoes").value = cadastro.observacoes;

    idEmEdicao = id;
    mensagemCadastro.textContent = "Editando o cadastro de " + cadastro.nome + ".";
    window.scrollTo({ top: 0, behavior: "smooth" });
}

function excluirCadastro(id) {
    cadastros = cadastros.filter(item => item.id !== id);
    atualizarTabela();
}

function visualizarCadastro(id) {
    const cadastro = cadastros.find(item => item.id === id);

    if (!cadastro) {
        return;
    }

    dadosVisualizacao.innerHTML = `
        ${criarDadoModal("Nome", cadastro.nome)}
        ${criarDadoModal("E-mail", cadastro.email)}
        ${criarDadoModal("Telefone", cadastro.telefone)}
        ${criarDadoModal("Empresa", cadastro.empresa)}
        ${criarDadoModal("Cargo", cadastro.cargo)}
        ${criarDadoModal("Cidade", cadastro.cidade)}
        ${criarDadoModal("Estado", cadastro.estado)}
        ${criarDadoModal("Observações", cadastro.observacoes || "Sem observações")}
        ${criarDadoModal("Status", cadastro.status)}
        ${criarDadoModal("Mensagem", cadastro.mensagem)}
    `;

    modalVisualizar.classList.remove("escondida");
}

function criarDadoModal(titulo, valor) {
    return `
        <div class="dado-modal">
            <strong>${titulo}</strong>
            <span>${escaparHTML(String(valor))}</span>
        </div>
    `;
}

function escaparHTML(texto) {
    const elemento = document.createElement("div");
    elemento.textContent = texto;
    return elemento.innerHTML;
}

function esperar(milissegundos) {
    return new Promise(resolve => setTimeout(resolve, milissegundos));
}

atualizarTabela();
