from sqlmodel import SQLModel, Field


class Usuario(SQLModel, table=True):
    username: str = Field(
        primary_key=True,
        index=True,
        max_length=50
    )

    senha_hash: str
    role: str
    mfa_enabled: bool = False

class Token(SQLModel):
    access_token: str
    token_type: str

class UsuarioResponse(SQLModel):
    username: str
    role: str
    mfa_enabled: bool