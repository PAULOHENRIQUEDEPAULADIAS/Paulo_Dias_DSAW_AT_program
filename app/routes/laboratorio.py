from fastapi import APIRouter, Depends

from app.auth.dependencies import require_scope
from app.database.database import consultas

router = APIRouter(
    prefix="/laboratorio",
    tags=["Laboratório"]
)


@router.get("/consultas")
def consultar_consultas(
    token=Depends(
        require_scope("consultas:leitura")
    )
):
    return consultas