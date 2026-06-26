from fastapi import FastAPI
from backend.app.database import engine, Base
from backend.app.models import barbeiro, cliente, agendamentos
from backend.app.routes import agendamento_routes

# Cria todas as tabelas no banco de dados automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(agendamento_routes.router)

@app.get("/")
def hello_world():
    return {
        "mensagem": "Barbearia API funcionando!"
    }