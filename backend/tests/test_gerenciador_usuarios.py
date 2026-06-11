import pytest

from app.domain.excecoes import DadosInvalidosError, EmailDuplicadoError
from app.repository.usuario_repository import UsuarioRepository
from app.service.gerenciador_usuarios import GerenciadorUsuarios


@pytest.fixture
def gerenciador() -> GerenciadorUsuarios:
    return GerenciadorUsuarios(UsuarioRepository())


def test_deve_retornar_lista_vazia_quando_nao_houver_usuarios(
    gerenciador: GerenciadorUsuarios,
) -> None:
    assert gerenciador.listar_usuarios() == []


def test_deve_adicionar_usuario_com_sucesso(gerenciador: GerenciadorUsuarios) -> None:
    usuario = gerenciador.adicionar_usuario("Ana Silva", "ana@email.com")

    usuarios = gerenciador.listar_usuarios()

    assert len(usuarios) == 1
    assert usuarios[0].id == usuario.id
    assert usuarios[0].nome == "Ana Silva"
    assert usuarios[0].email == "ana@email.com"


def test_deve_rejeitar_usuario_com_nome_vazio(gerenciador: GerenciadorUsuarios) -> None:
    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_usuario("   ", "ana@email.com")


def test_deve_rejeitar_usuario_com_email_duplicado(
    gerenciador: GerenciadorUsuarios,
) -> None:
    gerenciador.adicionar_usuario("Ana Silva", "ana@email.com")

    with pytest.raises(EmailDuplicadoError):
        gerenciador.adicionar_usuario("Bruno Costa", "ana@email.com")
