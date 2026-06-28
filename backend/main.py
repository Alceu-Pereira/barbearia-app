from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import engine, Base
from backend.app.models import barbeiro, cliente, agendamentos
from backend.app.routes import agendamento_routes
from backend.app.logger import logger

# Cria todas as tabelas no banco de dados automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(agendamento_routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    logger.info("Barbearia API iniciada com sucesso!")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Barbearia API encerrada")

@app.get("/")
def hello_world():
    logger.info("Rota raiz acessada")
    return {
        "mensagem": "Barbearia API funcionando!"
    }