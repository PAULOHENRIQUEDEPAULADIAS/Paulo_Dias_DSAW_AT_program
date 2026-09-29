from pydantic import BaseModel


class Usuario(BaseModel):
    username: str
    senha_hash: str
    role: str
    mfa_enabled: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str

class UsuarioResponse(BaseModel):
    username: str
    role: str
    mfa_enabled: bool