from pydantic import BaseModel, ConfigDict
from datetime import datetime

class AgendamentoBase(BaseModel):
    barbeiro_id: int
    cliente_id: int
    data_hora: datetime

class AgendamentoCreate(AgendamentoBase):
    pass

class AgendamentoResponse(AgendamentoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str