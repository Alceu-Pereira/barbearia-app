const API_URL = "http://127.0.0.1:8000"
let token = localStorage.getItem("cliente_token")
let clienteId = localStorage.getItem("cliente_id")
let clienteNome = localStorage.getItem("cliente_nome")

// ─── INICIALIZAÇÃO ─────────────────────────────────
function init() {
    if (token && clienteId) {
        mostrarAreaCliente()
    }
}

function mostrarAreaCliente() {
    document.getElementById("tela-auth").style.display = "none"
    document.getElementById("area-cliente").style.display = "block"
    document.getElementById("nome-cliente").textContent = `Olá, ${clienteNome}!`
    setTimeout(() => {
        carregarBarbeiros()
        carregarMeusAgendamentos()
    }, 300)
}

// ─── ABAS ──────────────────────────────────────────
function mostrarAba(aba) {
    document.getElementById("form-login").style.display = aba === "login" ? "block" : "none"
    document.getElementById("form-registro").style.display = aba === "registro" ? "block" : "none"
    document.getElementById("aba-login").classList.toggle("ativa", aba === "login")
    document.getElementById("aba-registro").classList.toggle("ativa", aba === "registro")
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
            mostrarAreaCliente()
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
    document.getElementById("area-cliente").style.display = "none"
}

// ─── BARBEIROS ─────────────────────────────────────
async function carregarBarbeiros() {
    const select = document.getElementById("barbeiro-select")
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

// ─── CRIAR AGENDAMENTO ─────────────────────────────
async function criarAgendamento() {
    const barbeiro_id = document.getElementById("barbeiro-select").value
    const data_hora = document.getElementById("data-hora").value
    const feedback = document.getElementById("agendamento-feedback")

    if (!data_hora) {
        feedback.textContent = "Selecione uma data e hora!"
        feedback.className = "erro"
        return
    }

    const dados = {
        barbeiro_id: parseInt(barbeiro_id),
        cliente_id: parseInt(clienteId),
        data_hora: new Date(data_hora).toISOString()
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
            feedback.textContent = "Agendamento criado com sucesso! ✅"
            feedback.className = "sucesso"
            carregarMeusAgendamentos()
        } else {
            feedback.textContent = resultado.detail
            feedback.className = "erro"
        }

    } catch (e) {
        feedback.textContent = "Erro ao conectar com o servidor."
        feedback.className = "erro"
    }
}

// ─── MEUS AGENDAMENTOS ─────────────────────────────
async function carregarMeusAgendamentos() {
    const lista = document.getElementById("lista-meus-agendamentos")
    if (!lista) return

    try {
        const resposta = await fetch(`${API_URL}/clientes/meus-agendamentos/${clienteId}`)
        const agendamentos = await resposta.json()

        if (agendamentos.length === 0) {
            lista.innerHTML = `<p class="vazio">Nenhum agendamento encontrado.</p>`
            return
        }

        lista.innerHTML = agendamentos.map(a => `
            <div class="agendamento-item">
                <div class="agendamento-info">
                    <strong>Agendamento #${a.id}</strong>
                    <p>📅 ${new Date(a.data_hora).toLocaleString("pt-BR")}</p>
                    <p>💈 Barbeiro #${a.barbeiro_id}</p>
                </div>
                <div style="display:flex; align-items:center;">
                    <span class="status ${a.status}">${a.status}</span>
                    ${a.status === "confirmado" ? `
                        <button class="btn-cancelar" onclick="cancelarAgendamento(${a.id})">
                            Cancelar
                        </button>` : ""
                    }
                </div>
            </div>
        `).join("")

    } catch (e) {
        lista.innerHTML = `<p class="vazio">Erro ao carregar agendamentos.</p>`
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
            carregarMeusAgendamentos()
        }

    } catch (e) {
        alert("Erro ao conectar com o servidor.")
    }
}

init()