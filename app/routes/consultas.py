
from fastapi import ( APIRouter, Request, Depends, HTTPException)
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from app.database.database import get_db
from app.auth.dependencies import ( get_current_user, require_consulta_owner, require_role)
from app.models.consulta import ( Consulta, ConsultaCreate, ConsultaResponse)
from app.models.usuario import Usuario
from app.rate_limit import limiter


router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_model=list[ConsultaResponse])
@limiter.limit("60/minute")
def listar_consultas(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):

    statement = select(Consulta)

    if current_user.role != "admin":
        statement = statement.where(
            Consulta.owner_username == current_user.username
        )

    return db.exec(statement).all()


@router.get("/pagina")
@limiter.limit("60/minute")
def pagina_consultas(
    request: Request,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):

    statement = select(Consulta)

    if current_user.role != "admin":
        statement = statement.where(
            Consulta.owner_username == current_user.username
        )

    consultas = db.exec(statement).all()

    return templates.TemplateResponse(
        request=request,
        name="consultas.html",
        context={
            "consultas": consultas,
            "current_user": current_user
        }
    )


@router.get("/{consulta_id}", response_model=ConsultaResponse)
@limiter.limit("60/minute")
def obter_consulta(
    request: Request,
    consulta=Depends(require_consulta_owner)
):
    return consulta


@router.post("/", response_model=ConsultaResponse, status_code=201)
@limiter.limit("60/minute")
def criar_consulta(
    request: Request,
    dados: ConsultaCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(
        require_role("medico", "admin")
    ),
):

    nova = Consulta(
        paciente=dados.paciente,
        especialidade=dados.especialidade,
        observacao_interna="",
        owner_username=current_user.username,
    )

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova