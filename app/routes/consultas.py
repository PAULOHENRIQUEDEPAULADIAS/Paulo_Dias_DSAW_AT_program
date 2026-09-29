from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.templating import Jinja2Templates

from app.auth.dependencies import get_current_user, require_role
from app.database.database import consultas
from app.models.consulta import ConsultaResponse
from app.models.usuario import Usuario
from app.database.database import usuarios



router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"]
)


@router.get("/",response_model=list[ConsultaResponse])
def listar_consultas(current_user: Usuario = Depends(get_current_user)):
    if current_user.role == "admin":
        return consultas
    return [
        consulta
        for consulta in consultas
        if consulta.owner_username == current_user.username
    ]

@router.get("/pagina")
def pagina_consultas(request: Request):
    return Jinja2Templates.templates.TemplateResponse(
        request=request,
        name="consultas.html",
        context={"consultas": consultas}
    )

@router.get("/{consulta_id}",response_model=ConsultaResponse)
def obter_consulta(consulta_id: int,current_user: Usuario = Depends(get_current_user)):
    consulta = next(
        (
            consulta
            for consulta in consultas
            if consulta.id == consulta_id
        ),
        None
    )

    if consulta is None:
        raise HTTPException(
            status_code=404,
            detail="Consulta não encontrada"
        )

    if (
        current_user.role != "admin"
        and consulta.owner_username != current_user.username
    ):
        raise HTTPException(
            status_code=403,
            detail="Acesso negado"
        )

    return consulta

@router.get("/usuarios")
def listar_usuarios(current_user=Depends(require_role("admin"))):
    return usuarios