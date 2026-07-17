import pytest

from app.domain.excecoes import DadosInvalidosError, EmailDuplicadoError, LoginDuplicadoError
from app.infra.repositories.usuario_repository import UsuarioArquivoBinarioRepository, UsuarioRepository
from app.business.services.gerenciador_usuarios import GerenciadorUsuarios


@pytest.fixture
def gerenciador() -> GerenciadorUsuarios:
    return GerenciadorUsuarios(UsuarioRepository())


def test_deve_retornar_lista_vazia_quando_nao_houver_usuarios(
    gerenciador: GerenciadorUsuarios,
) -> None:
    assert gerenciador.listar_usuarios() == []


def test_deve_adicionar_usuario_com_sucesso(gerenciador: GerenciadorUsuarios) -> None:
    usuario = gerenciador.adicionar_usuario(
        "Ana Silva",
        "ana@email.com",
        "anasilva",
        "Senha123",
    )

    usuarios = gerenciador.listar_usuarios()

    assert len(usuarios) == 1
    assert usuarios[0].id == usuario.id
    assert usuarios[0].nome == "Ana Silva"
    assert usuarios[0].email == "ana@email.com"
    assert usuarios[0].login == "anasilva"
    assert usuarios[0].senha == "Senha123"
    assert usuarios[0].perfil == "cliente"


def test_deve_cadastrar_usuario_com_perfil_gerente(
    gerenciador: GerenciadorUsuarios,
) -> None:
    gerente = gerenciador.adicionar_usuario(
        "Ana Silva", "ana@email.com", "anasilva", "Senha123", "gerente"
    )

    assert gerente.perfil == "gerente"


def test_deve_rejeitar_usuario_com_nome_vazio(gerenciador: GerenciadorUsuarios) -> None:
    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_usuario("   ", "ana@email.com", "anasilva", "Senha123")


def test_deve_rejeitar_usuario_com_email_duplicado(
    gerenciador: GerenciadorUsuarios,
) -> None:
    gerenciador.adicionar_usuario("Ana Silva", "ana@email.com", "anasilva", "Senha123")

    with pytest.raises(EmailDuplicadoError):
        gerenciador.adicionar_usuario("Bruno Costa", "ana@email.com", "bruno", "Senha123")


def test_deve_rejeitar_login_vazio(gerenciador: GerenciadorUsuarios) -> None:
    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_usuario("Ana Silva", "ana@email.com", "   ", "Senha123")


def test_deve_rejeitar_login_com_mais_de_12_caracteres(
    gerenciador: GerenciadorUsuarios,
) -> None:
    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_usuario("Ana Silva", "ana@email.com", "loginmuitogrande", "Senha123")


def test_deve_rejeitar_login_com_numero(gerenciador: GerenciadorUsuarios) -> None:
    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_usuario("Ana Silva", "ana@email.com", "ana1", "Senha123")


def test_deve_rejeitar_login_duplicado(gerenciador: GerenciadorUsuarios) -> None:
    gerenciador.adicionar_usuario("Ana Silva", "ana@email.com", "anasilva", "Senha123")

    with pytest.raises(LoginDuplicadoError):
        gerenciador.adicionar_usuario("Bruno Costa", "bruno@email.com", "anasilva", "Senha123")


def test_deve_rejeitar_senha_com_menos_de_8_caracteres(
    gerenciador: GerenciadorUsuarios,
) -> None:
    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_usuario("Ana Silva", "ana@email.com", "anasilva", "Sen123")


def test_deve_rejeitar_senha_com_mais_de_128_caracteres(
    gerenciador: GerenciadorUsuarios,
) -> None:
    senha = "A" * 129

    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_usuario("Ana Silva", "ana@email.com", "anasilva", senha)


def test_deve_rejeitar_senha_com_menos_de_3_grupos_aws(
    gerenciador: GerenciadorUsuarios,
) -> None:
    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_usuario("Ana Silva", "ana@email.com", "anasilva", "senhasimples")


def test_deve_persistir_usuarios_em_arquivo_binario(tmp_path) -> None:
    caminho_arquivo = tmp_path / "usuarios.bin"
    repositorio = UsuarioArquivoBinarioRepository(str(caminho_arquivo))
    gerenciador = GerenciadorUsuarios(repositorio)

    gerenciador.adicionar_usuario("Ana Silva", "ana@email.com", "anasilva", "Senha123")

    novo_repositorio = UsuarioArquivoBinarioRepository(str(caminho_arquivo))
    novo_gerenciador = GerenciadorUsuarios(novo_repositorio)

    usuarios = novo_gerenciador.listar_usuarios()

    assert len(usuarios) == 1
    assert usuarios[0].nome == "Ana Silva"
    assert usuarios[0].login == "anasilva"
