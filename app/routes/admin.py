from fastapi import APIRouter, Depends

from app.auth.dependencies import require_role
from app.database.database import usuarios
from app.models.usuario import UsuarioResponse

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/usuarios", response_model=list[UsuarioResponse])
def listar_usuarios(_=Depends(require_role("admin"))):
    return usuarios