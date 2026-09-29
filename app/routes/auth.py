import hmac
from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.security import (create_access_token,verify_password)
from app.database.database import usuarios
from app.config import settings



router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    otp: str | None = Form(default=None),
):
    user = next((u for u in usuarios if u.username == form_data.username), None)

    if user is None or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuário ou senha inválidos")

    if user.mfa_enabled:
        if otp is None or not hmac.compare_digest(otp, settings.mfa_demo_code):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Código MFA inválido ou ausente")

    token = create_access_token(username=user.username, role=user.role)
    return {"access_token": token, "token_type": "bearer"}

