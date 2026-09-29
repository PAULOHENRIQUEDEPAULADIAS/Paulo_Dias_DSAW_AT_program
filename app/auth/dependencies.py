from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt

from app.auth.security import (
    ALGORITHM,
    SECRET_KEY,
    oauth2_scheme
)
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
            SECRET_KEY,
            algorithms=[ALGORITHM]
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

def require_role(required_role: str):
    def role_checker(
        current_user=Depends(get_current_user)
    ):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso negado"
            )

        return current_user

    return role_checker

