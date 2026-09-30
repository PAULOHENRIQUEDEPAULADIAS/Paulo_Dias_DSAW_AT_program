from app.models.consulta import Consulta
from app.models.usuario import Usuario
from app.auth.security import hash_password


usuarios = [
    Usuario(
        username="admin",
        senha_hash=hash_password("senha1"),
        role="admin",
        mfa_enabled=True
    ),
    Usuario(
        username="dr.joao",
        senha_hash=hash_password("senha2"),
        role="medico",
        mfa_enabled=True
    ),
    Usuario(
        username="recepcao",
        senha_hash=hash_password("senha3"),
        role="recepcionista",
        mfa_enabled=False
    ),
]


consultas = [
    Consulta(
        id=1,
        paciente="João Silva",
        especialidade="Cardiologia",
        observacao_interna="Informação interna",
        owner_username="dr.joao"
    ),
    Consulta(
        id=2,
        paciente="Maria Souza",
        especialidade="Dermatologia",
        observacao_interna="Informação confidencial",
        owner_username="admin"
    ),
]

clientes_m2m = {
    "laboratorio_xyz": {
        "client_secret": "segredo-laboratorio",
        "scopes": [
            "consultas:leitura"
        ]
    }
}