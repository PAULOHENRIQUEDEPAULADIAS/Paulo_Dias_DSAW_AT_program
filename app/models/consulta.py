from typing import Literal

from pydantic import ConfigDict, field_validator
from sqlmodel import SQLModel, Field


class Consulta(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    paciente: str = Field(min_length=3, max_length=100)

    especialidade: str = Field(max_length=50)

    observacao_interna: str = Field(default="")

    owner_username: str = Field(
        foreign_key="usuario.username",
        index=True
    )


class ConsultaResponse(SQLModel):
    id: int
    paciente: str
    especialidade: str

class ConsultaCreate(SQLModel):
    model_config = ConfigDict(extra="forbid")

    paciente: str = Field(
        min_length=3,
        max_length=100,
    )

    especialidade: Literal[
        "Cardiologia",
        "Dermatologia",
        "Ortopedia",
        "Clínica Geral",
    ]

    @field_validator("paciente")
    @classmethod
    def validar_paciente(cls, valor):
        import re

        if not re.fullmatch(r"[A-Za-zÀ-ÖØ-öø-ÿ' -]+", valor):
            raise ValueError("Nome do paciente contém caracteres inválidos")

        return valor