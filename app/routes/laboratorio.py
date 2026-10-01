from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.database.database import get_db
from app.models.consulta import Consulta, ConsultaResponse
from app.auth.dependencies import require_scope
from app.rate_limit import limiter

router = APIRouter(
    prefix="/laboratorio",
    tags=["Laboratório"]
)


@router.get("/consultas", response_model=list[ConsultaResponse])
@limiter.limit("60/minute")
def consultar_consultas(request: Request,db: Session = Depends(get_db),
                        token=Depends(require_scope("consultas:leitura"))
):
    return db.exec(
        select(Consulta)
    ).all()