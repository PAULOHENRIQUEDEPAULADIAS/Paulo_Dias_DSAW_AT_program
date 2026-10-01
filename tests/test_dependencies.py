from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.auth.dependencies import (
    get_current_user,
    require_role,
    require_consulta_owner,
)
from app.models.usuario import Usuario
from app.models.consulta import Consulta


def test_get_current_user_com_usuario_existente(monkeypatch):
    usuario = Usuario(
        username="dr.joao",
        role="medico",
        senha_hash="hash-teste"
    )

    db = MagicMock()
    resultado = MagicMock()
    resultado.first.return_value = usuario
    db.exec.return_value = resultado

    monkeypatch.setattr(
        "app.auth.dependencies.jwt.decode",
        lambda *args, **kwargs: {"sub": "dr.joao"}
    )

    resultado_funcao = get_current_user(
        token="token-falso",
        db=db
    )

    assert resultado_funcao.username == "dr.joao"
    db.exec.assert_called_once()


def test_get_current_user_usuario_inexistente(monkeypatch):
    db = MagicMock()
    resultado = MagicMock()
    resultado.first.return_value = None
    db.exec.return_value = resultado

    monkeypatch.setattr(
        "app.auth.dependencies.jwt.decode",
        lambda *args, **kwargs: {"sub": "usuario-inexistente"}
    )

    with pytest.raises(HTTPException) as exc:
        get_current_user(token="token-falso", db=db)

    assert exc.value.status_code == 401


def test_require_role_permite_role_autorizada():
    usuario = MagicMock()
    usuario.role = "medico"

    checker = require_role("medico", "admin")
    resultado = checker(current_user=usuario)

    assert resultado == usuario


def test_require_role_bloqueia_role_nao_autorizada():
    usuario = MagicMock()
    usuario.role = "recepcionista"

    checker = require_role("medico", "admin")

    with pytest.raises(HTTPException) as exc:
        checker(current_user=usuario)

    assert exc.value.status_code == 403


def test_consulta_owner_permite_proprietario():
    usuario = MagicMock()
    usuario.username = "dr.joao"
    usuario.role = "medico"

    consulta = MagicMock(spec=Consulta)
    consulta.owner_username = "dr.joao"

    db = MagicMock()
    db.get.return_value = consulta

    resultado = require_consulta_owner(
        consulta_id=1,
        current_user=usuario,
        db=db
    )

    assert resultado == consulta


def test_consulta_owner_bloqueia_outro_usuario():
    usuario = MagicMock()
    usuario.username = "dr.maria"
    usuario.role = "medico"

    consulta = MagicMock(spec=Consulta)
    consulta.owner_username = "dr.joao"

    db = MagicMock()
    db.get.return_value = consulta

    with pytest.raises(HTTPException) as exc:
        require_consulta_owner(
            consulta_id=1,
            current_user=usuario,
            db=db
        )

    assert exc.value.status_code == 403


def test_consulta_owner_permite_admin():
    usuario = MagicMock()
    usuario.username = "admin"
    usuario.role = "admin"

    consulta = MagicMock(spec=Consulta)
    consulta.owner_username = "dr.joao"

    db = MagicMock()
    db.get.return_value = consulta

    resultado = require_consulta_owner(
        consulta_id=1,
        current_user=usuario,
        db=db
    )

    assert resultado == consulta