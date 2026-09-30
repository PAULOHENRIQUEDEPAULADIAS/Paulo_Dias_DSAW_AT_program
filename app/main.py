from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.consultas import router as consultas_router
from app.routes.admin import router as admin_router
from app.routes.laboratorio import router as laboratorio_router


app = FastAPI(
    title="API de Consultas",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(consultas_router)
app.include_router(admin_router)
app.include_router(laboratorio_router)