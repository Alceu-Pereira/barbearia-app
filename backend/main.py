from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.database import engine, Base
from backend.app.models import barbeiro, cliente, agendamentos, usuario
from backend.app.routes import agendamento_routes, auth_routes, barbeiro_routes, cliente_routes
from backend.app.logger import logger
from backend.app.scheduler import iniciar_scheduler

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Barbearia API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://barbearia-app-tau.vercel.app"
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agendamento_routes.router)
app.include_router(auth_routes.router)
app.include_router(barbeiro_routes.router)
app.include_router(cliente_routes.router)

@app.on_event("startup")
async def startup():
    logger.info("Barbearia API iniciada com sucesso!")
    iniciar_scheduler()

@app.on_event("shutdown")
async def shutdown():
    logger.info("Barbearia API encerrada.")

@app.get("/")
def hello_world():
    logger.info("Rota raiz acessada")
    return {"mensagem": "Barbearia API funcionando!"}