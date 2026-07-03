const API_URL = "http://127.0.0.1:8000"
let token = localStorage.getItem("token")

// ─── INICIALIZAÇÃO ─────────────────────────────────
function init() {
    if (token) {
        mostrarPainel()
    } else {
        mostrarLogin()
    }
}

function mostrarLogin() {
    document.getElementById("tela-login").style.display = "flex"
    document.getElementById("painel").style.display = "none"
}

function mostrarPainel() {
    document.getElementById("tela-login").style.display = "none"
    document.getElementById("painel").style.display = "block"
    setTimeout(() => carregarDados(), 300)
}

function carregarDados() {
    listarAgendamentos()
    listarBarbeiros()
    listarClientes()
}

// ─── LOGIN ─────────────────────────────────────────
async function login() {
    const email = document.getElementById("login-email").value
    const senha = document.getElementById("login-senha").value
    const erro = document.getElementById("login-erro")

    const formData = new FormData()
    formData.append("username", email)
    formData.append("password", senha)

    try {
        const resposta = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            body: formData
        })

        const resultado = await resposta.json()

        if (resposta.ok) {
            token = resultado.access_token
            localStorage.setItem("token", token)
            erro.textContent = ""
            mostrarPainel()
        } else {
            erro.textContent = "Email ou senha incorretos."
        }

    } catch (e) {
        erro.textContent = "Erro ao conectar com o servidor."
    }
}

function logout() {
    localStorage.removeItem("token")
    token = null
    mostrarLogin()
}

// ─── AGENDAMENTOS ──────────────────────────────────
async function listarAgendamentos() {
    const lista = document.getElementById("lista-agendamentos-hoje")

    if (!lista) return

    try {
        const resposta = await fetch(`${API_URL}/agendamentos/`)
        const agendamentos = await resposta.json()

        const hoje = new Date().toLocaleDateString("pt-BR")
        const deHoje = agendamentos.filter(a => {
            const data = new Date(a.data_hora).toLocaleDateString("pt-BR")
            return data === hoje
        })

        if (deHoje.length === 0) {
            lista.innerHTML = `<p class="vazio">Nenhum agendamento para hoje.</p>`
            return
        }

        lista.innerHTML = deHoje.map(a => `
            <div class="item-lista">
                <div>
                    <strong>Agendamento #${a.id}</strong>
                    <p>📅 ${new Date(a.data_hora).toLocaleTimeString("pt-BR")} · 
                       💈 Barbeiro #${a.barbeiro_id} · 
                       👤 Cliente #${a.cliente_id}</p>
                </div>
                <span class="status ${a.status}">${a.status}</span>
            </div>
        `).join("")

    } catch (e) {
        lista.innerHTML = `<p class="vazio">Erro ao carregar agendamentos.</p>`
    }
}

// ─── BARBEIROS ─────────────────────────────────────
async function listarBarbeiros() {
    const lista = document.getElementById("lista-barbeiros")

    if (!lista) return

    try {
        const resposta = await fetch(`${API_URL}/barbeiros/`)
        const barbeiros = await resposta.json()

        if (barbeiros.length === 0) {
            lista.innerHTML = `<p class="vazio">Nenhum barbeiro cadastrado.</p>`
            return
        }

        lista.innerHTML = barbeiros.map(b => `
            <div class="item-lista">
                <div>
                    <strong>${b.nome}</strong>
                    <p>${b.especialidade}</p>
                </div>
                <button class="btn-deletar" onclick="deletarBarbeiro(${b.id})">
                    Deletar
                </button>
            </div>
        `).join("")

    } catch (e) {
        lista.innerHTML = `<p class="vazio">Erro ao carregar barbeiros.</p>`
    }
}

async function criarBarbeiro() {
    const nome = document.getElementById("barbeiro-nome").value
    const especialidade = document.getElementById("barbeiro-especialidade").value

    if (!nome || !especialidade) {
        alert("Preencha nome e especialidade!")
        return
    }

    try {
        const resposta = await fetch(`${API_URL}/barbeiros/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ nome, especialidade })
        })

        if (resposta.ok) {
            document.getElementById("barbeiro-nome").value = ""
            document.getElementById("barbeiro-especialidade").value = ""
            listarBarbeiros()
        } else {
            const erro = await resposta.json()
            alert(erro.detail)
        }

    } catch (e) {
        alert("Erro ao conectar com o servidor.")
    }
}

async function deletarBarbeiro(id) {
    if (!confirm("Deseja deletar este barbeiro?")) return

    try {
        const resposta = await fetch(`${API_URL}/barbeiros/${id}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        })

        if (resposta.ok) {
            listarBarbeiros()
        }

    } catch (e) {
        alert("Erro ao conectar com o servidor.")
    }
}

// ─── CLIENTES ──────────────────────────────────────
async function listarClientes() {
    const lista = document.getElementById("lista-clientes")

    if (!lista) return

    try {
        const resposta = await fetch(`${API_URL}/clientes/`)
        const clientes = await resposta.json()

        if (clientes.length === 0) {
            lista.innerHTML = `<p class="vazio">Nenhum cliente cadastrado.</p>`
            return
        }

        lista.innerHTML = clientes.map(c => `
            <div class="item-lista">
                <div>
                    <strong>${c.nome}</strong>
                    <p>📱 ${c.telefone}</p>
                </div>
                <button class="btn-deletar" onclick="deletarCliente(${c.id})">
                    Deletar
                </button>
            </div>
        `).join("")

    } catch (e) {
        lista.innerHTML = `<p class="vazio">Erro ao carregar clientes.</p>`
    }
}

async function criarCliente() {
    const nome = document.getElementById("cliente-nome").value
    const telefone = document.getElementById("cliente-telefone").value

    if (!nome || !telefone) {
        alert("Preencha nome e telefone!")
        return
    }

    try {
        const resposta = await fetch(`${API_URL}/clientes/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ nome, telefone })
        })

        if (resposta.ok) {
            document.getElementById("cliente-nome").value = ""
            document.getElementById("cliente-telefone").value = ""
            listarClientes()
        } else {
            const erro = await resposta.json()
            alert(erro.detail)
        }

    } catch (e) {
        alert("Erro ao conectar com o servidor.")
    }
}

async function deletarCliente(id) {
    if (!confirm("Deseja deletar este cliente?")) return

    try {
        const resposta = await fetch(`${API_URL}/clientes/${id}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${token}` }
        })

        if (resposta.ok) {
            listarClientes()
        }

    } catch (e) {
        alert("Erro ao conectar com o servidor.")
    }
}

// ─── EVENTOS ───────────────────────────────────────
document.getElementById("btn-login").addEventListener("click", login)
document.getElementById("btn-logout").addEventListener("click", logout)
document.getElementById("btn-criar-barbeiro").addEventListener("click", criarBarbeiro)
document.getElementById("btn-criar-cliente").addEventListener("click", criarCliente)

init()