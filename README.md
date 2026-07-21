# Barbearia App

Sistema completo de agendamentos para barbearias, que resolve a dor comum
de gerenciar horários por WhatsApp, telefone ou papel.

Com ele, o dono da barbearia tem uma visão centralizada de todos os
agendamentos, e o cliente ganha autonomia para marcar, visualizar e
cancelar seus próprios horários — sem precisar ligar ou mandar mensagem
para confirmar disponibilidade.

Desenvolvido com Python, FastAPI e PostgreSQL.

## Tecnologias

- **Backend:** Python 3.14 + FastAPI
- **Banco de Dados:** PostgreSQL 18
- **Frontend:** HTML, CSS e JavaScript
- **Testes:** Pytest com 100% de cobertura
- **ORM:** SQLAlchemy

## Funcionalidades

### Cliente
- Criar conta própria
- Login e autenticação
- Criar agendamento
- Cancelar agendamento
- Visualizar apenas seus próprios agendamentos

### Admin
- Login administrativo
- Gerenciar barbeiros (criar, listar, editar, deletar)
- Gerenciar clientes (criar, listar, editar, deletar)
- Visualizar todos os agendamentos do sistema
- Cancelar qualquer agendamento

### Automações do Sistema
- Logs detalhados de todas as operações
- Email de confirmação ao criar agendamento
- Email de cancelamento ao cancelar agendamento
- Lembrete automático por email, 1 hora antes do horário agendado

## 🧠 Regras de Negócio

- Não é possível agendar em horário passado
- Não é possível agendar o mesmo barbeiro no mesmo horário
- Não é possível cancelar um agendamento já cancelado

## 📁 Estrutura do Projeto

arbearia-app/

├── backend/

│   ├── app/

│   │   ├── models/        # Modelos do banco de dados

│   │   ├── routes/        # Endpoints da API

│   │   ├── schemas/       # Validação de dados

│   │   ├── services/      # Regras de negócio

│   │   ├── database.py    # Conexão com banco

│   │   └── logger.py      # Sistema de logs

│   ├── tests/             # Testes unitários

│   └── main.py            # Ponto de entrada

└── frontend/

├── index.html

├── style.css

└── app.js

## ⚙️ Como rodar localmente

**1. Clone o repositório**
```bash
git clone https://github.com/Alceu-Pereira/barbearia-app.git
cd barbearia-app
```

**2. Crie e ative o ambiente virtual**
```bash
py -m venv venv
.\venv\Scripts\activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto: DATABASE_URL=postgresql://postgres:SUA_SENHA@127.0.0.1:5432/barbearia

**5. Inicie o servidor**
```bash
uvicorn backend.main:app --reload
```

**6. Acesse o sistema**
- Frontend: abra o arquivo `frontend/index.html` no navegador
- API Docs: http://127.0.0.1:8000/docs

## 🧪 Rodando os testes

```bash
pytest --cov=backend/app/services --cov-report=term-missing
```

## 👨‍💻 Autor

Desenvolvido por **Alceu Pereira**