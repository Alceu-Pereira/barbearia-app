# ✂️ Barbearia App

Sistema de agendamentos para barbearia desenvolvido com Python, FastAPI e PostgreSQL.

## 🚀 Tecnologias

- **Backend:** Python 3.14 + FastAPI
- **Banco de Dados:** PostgreSQL 18
- **Frontend:** HTML, CSS e JavaScript
- **Testes:** Pytest com 100% de cobertura
- **ORM:** SQLAlchemy

## ✨ Funcionalidades

- ✅ Criar agendamentos
- ✅ Listar agendamentos
- ✅ Cancelar agendamentos
- ✅ Validação de horários duplicados
- ✅ Validação de horários passados
- ✅ Sistema de logs

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