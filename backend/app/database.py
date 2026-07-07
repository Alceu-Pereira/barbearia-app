from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env
load_dotenv()

# Pega a URL do banco de dados do arquivo .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria a conexão do Python com o PostgreSQL
engine = create_engine(DATABASE_URL)

# Cria uma fábrica de sessões - cada requisição abre uma sessão, usa e fecha

# Evita o Connection Leak (múltiplas requisições sem encerrá-las)
SessionLocal = sessionmaker(bind=engine)

# Base que todos os models herdarão
Base = declarative_base()