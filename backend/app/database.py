from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Pega a URL do banco de dados do arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a conexão com o banco de dados
engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessões
SessionLocal = sessionmaker(bind=engine)

# Base que todos os models herdarão
Base = declarative_base()