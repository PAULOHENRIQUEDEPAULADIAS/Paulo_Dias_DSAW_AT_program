from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlmodel import Session, select

from app.auth.security import oauth2_scheme
from app.config import settings
from app.database.database import get_db
from app.models.usuario import Usuario
from app.models.consulta import Consulta

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
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

    user = db.exec(
        select(Usuario).where(
            Usuario.username == username
        )
    ).first()

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

def require_consulta_owner(
    consulta_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):

    consulta = db.get(Consulta, consulta_id)

    if consulta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Consulta não encontrada",
        )

    if current_user.role == "admin":
        return consulta

    if consulta.owner_username != current_user.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado",
        )

    return consulta
    