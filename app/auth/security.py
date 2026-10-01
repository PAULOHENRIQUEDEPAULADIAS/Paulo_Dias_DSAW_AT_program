from datetime import datetime, timedelta, timezone
from app.config import settings

from jose import jwt
import bcrypt
from fastapi.security import OAuth2PasswordBearer



def hash_password(password: str) -> str:
    senha_bytes = password.encode("utf-8")
    return bcrypt.hashpw(senha_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def create_access_token(username: str,role: str,expires_delta: timedelta | None = None):
    expire = datetime.now(timezone.utc) + (
        expires_delta
        or timedelta(minutes=settings.access_token_expire_minutes)
    )

    payload = {
        "sub": username,
        "role": role,
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)

def create_m2m_access_token(client_id: str,scopes: list[str]):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": client_id,
        "client_type": "m2m",
        "scope": " ".join(scopes),
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    