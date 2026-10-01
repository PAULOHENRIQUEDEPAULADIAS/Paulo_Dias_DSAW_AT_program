import hmac
from fastapi import APIRouter, Depends, HTTPException, Request, status, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.database.database import get_db, clientes_m2m
from app.models.usuario import Usuario
from app.auth.security import (create_access_token,verify_password)
from app.config import settings
from app.auth.security import create_m2m_access_token
from app.rate_limit import limiter



router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post("/token")
@limiter.limit("5/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    otp: str | None = Form(default=None),
    db: Session = Depends(get_db),
):
    user = db.exec(
    select(Usuario).where(
            Usuario.username == form_data.username
        )
    ).first()

    
    if user is None or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Usuário ou senha inválidos")

    if user.mfa_enabled:
        codigo = otp or form_data.client_secret
        if not codigo or not hmac.compare_digest(
            codigo.encode("utf-8"), settings.mfa_demo_code.encode("utf-8")):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Código MFA inválido ou ausente")

    token = create_access_token(username=user.username, role=user.role)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/token/m2m")
@limiter.limit("60/minute")
def token_m2m(request: Request, client_id: str = Form(...),client_secret: str = Form(...),scope: str = Form("")):
    cliente = clientes_m2m.get(client_id)

    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Cliente inválido"
        )

    if not hmac.compare_digest(
        client_secret,
        cliente["client_secret"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

    requested_scopes = scope.split()

    for requested_scope in requested_scopes:
        if requested_scope not in cliente["scopes"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Escopo não permitido: {requested_scope}"
            )

    token = create_m2m_access_token(
        client_id=client_id,
        scopes=requested_scopes
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60,
        "scope": " ".join(requested_scopes)
    }