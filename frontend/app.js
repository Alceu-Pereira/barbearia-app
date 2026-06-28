const API_URL = "https://barbearia-app-lrnx.onrender.com"

// ─── LISTAR AGENDAMENTOS ───────────────────────────────────────
async function listarAgendamentos() {
    const lista = document.getElementById("lista-agendamentos")

    try {
        const resposta = await fetch(`${API_URL}/agendamentos/`)
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
                    <p>💈 Barbeiro #${agendamento.barbeiro_id} · 👤 Cliente #${agendamento.cliente_id}</p>
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

// ─── CRIAR AGENDAMENTO ─────────────────────────────────────────
async function criarAgendamento() {
    const barbeiro_id = document.getElementById("barbeiro_id").value
    const cliente_id = document.getElementById("cliente_id").value
    const data_hora = document.getElementById("data_hora").value
    const feedback = document.getElementById("mensagem-feedback")

    if (!data_hora) {
        mostrarFeedback("Por favor, selecione uma data e hora.", "erro")
        return
    }

    const dados = {
        barbeiro_id: parseInt(barbeiro_id),
        cliente_id: parseInt(cliente_id),
        data_hora: new Date(data_hora).toISOString()
    }

    try {
        const resposta = await fetch(`${API_URL}/agendamentos/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
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

// ─── CANCELAR AGENDAMENTO ──────────────────────────────────────
async function cancelarAgendamento(id) {
    if (!confirm("Deseja cancelar este agendamento?")) return

    try {
        const resposta = await fetch(`${API_URL}/agendamentos/${id}/cancelar`, {
            method: "PATCH"
        })

        const resultado = await resposta.json()

        if (resposta.ok) {
            mostrarFeedback("Agendamento cancelado com sucesso! ✅", "sucesso")
            listarAgendamentos()
        } else {
            mostrarFeedback(resultado.detail, "erro")
        }

    } catch (erro) {
        mostrarFeedback("Erro ao conectar com o servidor.", "erro")
    }
}

// ─── FUNÇÕES AUXILIARES ────────────────────────────────────────
function formatarData(dataISO) {
    const data = new Date(dataISO)
    return data.toLocaleString("pt-BR")
}

function mostrarFeedback(mensagem, tipo) {
    const feedback = document.getElementById("mensagem-feedback")
    feedback.textContent = mensagem
    feedback.className = tipo
}

// ─── INICIALIZAÇÃO ─────────────────────────────────────────────
document.getElementById("btn-agendar").addEventListener("click", criarAgendamento)
listarAgendamentos()