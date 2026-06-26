from pydantic import BaseModel, field_validator
from datetime import datetime

class AgendamentoBase(BaseModel):
    barbeiro_id: int
    cliente_id: int
    data_hora: datetime

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoResponse(AgendamentoBase):
    id: int
    status: str

    class Config:
        from_attributes = True