from pydantic import BaseModel, ConfigDict


class Consulta(BaseModel):
    id: int
    paciente: str
    especialidade: str
    observacao_interna: str
    owner_username: str


class ConsultaResponse(BaseModel):
    id: int
    paciente: str
    especialidade: str

class ConsultaCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    paciente: str
    especialidade: str
