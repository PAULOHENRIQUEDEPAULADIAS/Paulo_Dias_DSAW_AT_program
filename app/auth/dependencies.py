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

