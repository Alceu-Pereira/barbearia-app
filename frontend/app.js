const API_URL = "http://127.0.0.1:8000"
let token = localStorage.getItem("cliente_token")
let clienteId = localStorage.getItem("cliente_id")
let clienteNome = localStorage.getItem("cliente_nome")

// ─── INICIALIZAÇÃO ─────────────────────────────────
function init() {
    if (token && clienteId) {
        mostrarAreaAgendamentos()
    }
}

function mostrarAreaAgendamentos() {
    document.getElementById("tela-auth").style.display = "none"
    document.getElementById("area-agendamentos").style.display = "block"
    document.getElementById("nome-cliente").textContent = `Olá, ${clienteNome}!`
    setTimeout(() => {
        carregarBarbeiros()
        listarAgendamentos()
    }, 300)
}

// ─── ABAS ──────────────────────────────────────────
function mostrarAba(aba) {
    document.getElementById("form-login").style.display = aba === "login" ? "block" : "none"
    document.getElementById("form-registro").style.display = aba === "registro" ? "block" : "none"

    const btnLogin = document.getElementById("aba-login")
    const btnRegistro = document.getElementById("aba-registro")

    if (aba === "login") {
        btnLogin.style.background = "#1a1a2e"
        btnLogin.style.color = "white"
        btnRegistro.style.background = "white"
        btnRegistro.style.color = "#666"
    } else {
        btnRegistro.style.background = "#1a1a2e"
        btnRegistro.style.color = "white"
        btnLogin.style.background = "white"
        btnLogin.style.color = "#666"
    }

    document.getElementById("auth-erro").textContent = ""
    document.getElementById("auth-sucesso").textContent = ""
}

// ─── LOGIN ─────────────────────────────────────────
async function login() {
    const email = document.getElementById("login-email").value
    const senha = document.getElementById("login-senha").value
    const erro = document.getElementById("auth-erro")

    const formData = new FormData()
    formData.append("username", email)
    formData.append("password", senha)

    try {
        const resposta = await fetch(`${API_URL}/clientes/login`, {
            method: "POST",
            body: formData
        })

        const resultado = await resposta.json()

        if (resposta.ok) {
            token = resultado.access_token
            clienteId = resultado.cliente_id
            clienteNome = resultado.nome

            localStorage.setItem("cliente_token", token)
            localStorage.setItem("cliente_id", clienteId)
            localStorage.setItem("cliente_nome", clienteNome)

            erro.textContent = ""
            mostrarAreaAgendamentos()
        } else {
            erro.textContent = resultado.detail || "Email ou senha incorretos."
        }

    } catch (e) {
        erro.textContent = "Erro ao conectar com o servidor."
    }
}

// ─── REGISTRO ──────────────────────────────────────
async function registrar() {
    const nome = document.getElementById("reg-nome").value
    const telefone = document.getElementById("reg-telefone").value
    const email = document.getElementById("reg-email").value
    const senha = document.getElementById("reg-senha").value
    const erro = document.getElementById("auth-erro")
    const sucesso = document.getElementById("auth-sucesso")

    try {
        const resposta = await fetch(`${API_URL}/clientes/registro`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ nome, telefone, email, senha })
        })

        const resultado = await resposta.json()

        if (resposta.ok) {
            erro.textContent = ""
            sucesso.textContent = "Conta criada com sucesso! Faça login."
            mostrarAba("login")
        } else {
            sucesso.textContent = ""
            erro.textContent = resultado.detail || "Erro ao criar conta."
        }

    } catch (e) {
        erro.textContent = "Erro ao conectar com o servidor."
    }
}

// ─── LOGOUT ────────────────────────────────────────
function logout() {
    localStorage.removeItem("cliente_token")
    localStorage.removeItem("cliente_id")
    localStorage.removeItem("cliente_nome")
    token = null
    clienteId = null
    clienteNome = null
    document.getElementById("tela-auth").style.display = "flex"
    document.getElementById("area-agendamentos").style.display = "none"
}

// ─── BARBEIROS ─────────────────────────────────────
async function carregarBarbeiros() {
    const select = document.getElementById("barbeiro_id")
    if (!select) return

    try {
        const resposta = await fetch(`${API_URL}/barbeiros/`)
        const barbeiros = await resposta.json()

        select.innerHTML = barbeiros.map(b =>
            `<option value="${b.id}">${b.nome} — ${b.especialidade}</option>`
        ).join("")

    } catch (e) {
        console.error("Erro ao carregar barbeiros:", e)
    }
}

// ─── LISTAR AGENDAMENTOS ───────────────────────────
async function listarAgendamentos() {
    const lista = document.getElementById("lista-agendamentos")
    if (!lista) return

    try {
        const resposta = await fetch(`${API_URL}/clientes/meus-agendamentos/${clienteId}`)
        const agendamentos = await resposta.json()

        if (agendamentos.length === 0) {
            lista.innerHTML = `<p class="vazio">Nenhum agendamento encontrado.</p>`
            return
        }

        lista.innerHTML = agendamentos.map(agendamento => `
            <div class="agendamento-item">
                <div class="agendamento-info">
                    <strong>Agendamento #${agendamento.id}</strong>
                    <p>📅 ${formatarData(agendamento.data_hora)}</p>
                    <p>💈 Barbeiro #${agendamento.barbeiro_id}</p>
                </div>
                <div style="display:flex; align-items:center;">
                    <span class="status ${agendamento.status}">${agendamento.status}</span>
                    ${agendamento.status === "confirmado" ? `
                        <button class="btn-cancelar" onclick="cancelarAgendamento(${agendamento.id})">
                            Cancelar
                        </button>` : ""
                    }
                </div>
            </div>
        `).join("")

    } catch (erro) {
        lista.innerHTML = `<p class="vazio">Erro ao carregar agendamentos.</p>`
    }
}

// ─── CRIAR AGENDAMENTO ─────────────────────────────
async function criarAgendamento() {
    const barbeiro_id = document.getElementById("barbeiro_id").value
    const data_hora = document.getElementById("data_hora").value
    const feedback = document.getElementById("mensagem-feedback")

    if (!data_hora) {
        mostrarFeedback("Por favor, selecione uma data e hora.", "erro")
        return
    }

    const dados = {
    barbeiro_id: parseInt(barbeiro_id),
    cliente_id: parseInt(clienteId),
    data_hora: data_hora
    }

    try {
        const resposta = await fetch(`${API_URL}/agendamentos/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(dados)
        })

        const resultado = await resposta.json()

        if (resposta.ok) {
            mostrarFeedback("Agendamento criado com sucesso! ✅", "sucesso")
            listarAgendamentos()
        } else {
            mostrarFeedback(resultado.detail, "erro")
        }

    } catch (erro) {
        mostrarFeedback("Erro ao conectar com o servidor.", "erro")
    }
}

// ─── CANCELAR AGENDAMENTO ──────────────────────────
async function cancelarAgendamento(id) {
    if (!confirm("Deseja cancelar este agendamento?")) return

    try {
        const resposta = await fetch(`${API_URL}/agendamentos/${id}/cancelar`, {
            method: "PATCH",
            headers: { "Authorization": `Bearer ${token}` }
        })

        if (resposta.ok) {
            mostrarFeedback("Agendamento cancelado com sucesso! ✅", "sucesso")
            listarAgendamentos()
        }

    } catch (erro) {
        mostrarFeedback("Erro ao conectar com o servidor.", "erro")
    }
}

// ─── FUNÇÕES AUXILIARES ────────────────────────────
function formatarData(dataISO) {
    const data = new Date(dataISO)
    return data.toLocaleString("pt-BR")
}

function mostrarFeedback(mensagem, tipo) {
    const feedback = document.getElementById("mensagem-feedback")
    feedback.textContent = mensagem
    feedback.className = tipo
}

init()