
from fastapi import APIRouter, Depends, Request
from sqlmodel import Session, select

from app.auth.dependencies import require_role
from app.database.database import get_db
from app.models.usuario import Usuario, UsuarioResponse
from app.rate_limit import limiter


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/usuarios",response_model=list[UsuarioResponse])
@limiter.limit("60/minute")
def listar_usuarios(request: Request,db: Session = Depends(get_db),_=Depends(require_role("admin"))):
    return db.exec(
        select(Usuario)
    ).all()