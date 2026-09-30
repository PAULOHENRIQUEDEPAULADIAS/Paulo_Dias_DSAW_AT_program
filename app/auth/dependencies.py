from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.auth.security import oauth2_scheme
from app.config import settings
from app.database.database import usuarios


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = next(
        (
            usuario
            for usuario in usuarios
            if usuario.username == username
        ),
        None
    )

    if user is None:
        raise credentials_exception

    return user

def require_role(*roles: str):
    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Acesso negado")
        return current_user
    return role_checker

def get_m2m_client(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token M2M inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        client_type = payload.get("client_type")
        client_id = payload.get("sub")

        if client_type != "m2m" or client_id is None:
            raise credentials_exception

        return payload

    except JWTError:
        raise credentials_exception


def require_scope(required_scope: str):
    def scope_checker(token_payload=Depends(get_m2m_client)):
        scopes = token_payload.get("scope", "").split()

        if required_scope not in scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Escopo insuficiente"
            )

        return token_payload

    return scope_checker

