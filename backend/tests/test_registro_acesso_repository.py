from datetime import datetime

from app.domain.registro_acesso import RegistroAcesso
from app.infra.repositories.registro_acesso_repository import RegistroAcessoRepository


def test_deve_retornar_lista_vazia_quando_nao_houver_registros() -> None:
    repositorio = RegistroAcessoRepository()

    assert repositorio.buscar_todos() == []


def test_deve_salvar_e_listar_registros_de_acesso() -> None:
    repositorio = RegistroAcessoRepository()
    registro = RegistroAcesso(
        id=repositorio.gerar_proximo_id(),
        usuario_id=1,
        login="anasilva",
        momento=datetime(2026, 7, 16, 10, 0, 0),
    )

    repositorio.salvar(registro)

    registros = repositorio.buscar_todos()
    assert len(registros) == 1
    assert registros[0].usuario_id == 1
    assert registros[0].login == "anasilva"


def test_gerar_proximo_id_incrementa_a_cada_chamada() -> None:
    repositorio = RegistroAcessoRepository()

    assert repositorio.gerar_proximo_id() == 1
    assert repositorio.gerar_proximo_id() == 2
