from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.routes.auth import router as auth_router
from app.routes.consultas import router as consultas_router
from app.routes.admin import router as admin_router
from app.routes.laboratorio import router as laboratorio_router
from app.config import settings
from app.rate_limit import limiter
from app.middleware.security_headers import SecurityHeadersMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    inicializar_dados()
    yield

app = FastAPI(
    title="API de Consultas",
    version="1.0.0",
    lifespan=lifespan
)


app.include_router(auth_router)
app.include_router(consultas_router)
app.include_router(admin_router)
app.include_router(laboratorio_router)
app.add_middleware(SecurityHeadersMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)

from app.database.database import (
    create_db_and_tables,
    inicializar_dados
)