from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.security import (create_access_token,verify_password)
from app.database.database import usuarios


router = APIRouter(
    prefix="/auth",
    tags=["Autenticação"]
)


@router.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = next(
        (
            usuario
            for usuario in usuarios
            if usuario.username == form_data.username
        ),
        None
    )

    if user is None or not verify_password(
        form_data.password,
        user.senha_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos"
        )

    token = create_access_token(
        username=user.username,
        role=user.role
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

