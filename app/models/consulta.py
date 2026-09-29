from pydantic import BaseModel


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