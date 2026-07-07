# Importa as ferramentas que precisamos para definir colunas e tipos de dados
from sqlalchemy import Column, Integer, String, Boolean

# Importa a base - molde pai que diz ao SQLAlchemy que essa classe é uma tabela.
from backend.app.database import Base

# Cria uma classe chamada Barbeiro que herda da Base - ou seja, ela representa uma tabela.
class Barbeiro(Base):

    # O nome desta tabela no PostgreSQL será barbeiros.
    __tablename__ = "barbeiros"

    # Coluna id do tipo inteiro, é a chave primaria e tem índice para buscas rápidas.
    id = Column(Integer, primary_key=True, index=True)

    # Coluna nome do tipo string, não pode ser vazia.
    nome = Column(String, nullable=False)

    # Coluna especialidade do tipo string, não pode ser vazia.
    especialidade = Column(String, nullable=False)

    # Coluna ativo do tipo verdadeiro/falso, começa com True como padrão.
    # Hard delete x Soft delete aplicado.
    ativo = Column(Boolean, default=True)


