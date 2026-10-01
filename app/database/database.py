# from app.models.consulta import Consulta
# from app.models.usuario import Usuario
# from app.auth.security import hash_password
from app.config import settings


# usuarios = [
#     Usuario(
#         username="admin",
#         senha_hash=hash_password(settings.admin_password),
#         role="admin",
#         mfa_enabled=True
#     ),
#     Usuario(
#         username="dr.joao",
#         senha_hash=hash_password(settings.dr_joao_password),
#         role="medico",
#         mfa_enabled=False
#     ),
#     Usuario(
#         username="recepcao",
#         senha_hash=hash_password(settings.recepcao_password),
#         role="recepcionista",
#         mfa_enabled=False
#     ),
# ]


# consultas = [
#     Consulta(
#         id=1,
#         paciente="João Silva",
#         especialidade="Cardiologia",
#         observacao_interna="Informação interna",
#         owner_username="dr.joao"
#     ),
#     Consulta(
#         id=2,
#         paciente="Maria Souza",
#         especialidade="Dermatologia",
#         observacao_interna="Informação confidencial",
#         owner_username="admin"
#     ),
# ]

from sqlmodel import SQLModel, Session, create_engine, select

from app.models.usuario import Usuario
from app.models.consulta import Consulta
from app.auth.security import hash_password

connect_args = {}

if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}


engine = create_engine(
    settings.database_url,
    echo=False,
    connect_args=connect_args
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session

def inicializar_dados():
    with Session(engine) as session:

        usuarios_iniciais = [
            Usuario(
                username="admin",
                senha_hash=hash_password(settings.admin_password),
                role="admin",
                mfa_enabled=True
            ),
            Usuario(
                username="dr.joao",
                senha_hash=hash_password(settings.dr_joao_password),
                role="medico",
                mfa_enabled=False
            ),
            Usuario(
                username="recepcao",
                senha_hash=hash_password(settings.recepcao_password),
                role="recepcionista",
                mfa_enabled=False
            ),
        ]

        for usuario in usuarios_iniciais:
            existente = session.get(Usuario, usuario.username)

            if existente is None:
                session.add(usuario)

        session.commit()

        consultas_iniciais = [
            Consulta(
                paciente="João Silva",
                especialidade="Cardiologia",
                observacao_interna="Informação interna",
                owner_username="dr.joao"
            ),
            Consulta(
                paciente="Maria Souza",
                especialidade="Dermatologia",
                observacao_interna="Informação confidencial",
                owner_username="admin"
            ),
        ]

        for consulta in consultas_iniciais:
            existente = session.exec(
                select(Consulta).where(
                    Consulta.paciente == consulta.paciente,
                    Consulta.owner_username == consulta.owner_username
                )
            ).first()

            if existente is None:
                session.add(consulta)

        session.commit()


clientes_m2m = {
    "laboratorio_xyz": {
        "client_secret": settings.laboratorio_client_secret,
        "scopes": [
            "consultas:leitura"
        ]
    }
}