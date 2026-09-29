from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.consultas import router as consultas_router


app = FastAPI(
    title="API de Consultas",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(consultas_router)