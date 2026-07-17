import pytest

from app.business.services.facade_controller import FacadeSingletonController


@pytest.fixture
def facade() -> FacadeSingletonController:
    FacadeSingletonController.resetar_instancia()
    return FacadeSingletonController.obter_instancia()


def test_deve_ser_singleton() -> None:
    FacadeSingletonController.resetar_instancia()

    primeira = FacadeSingletonController.obter_instancia()
    segunda = FacadeSingletonController.obter_instancia()
    terceira = FacadeSingletonController()

    assert primeira is segunda
    assert primeira is terceira


def test_quantidade_entidades_inicia_em_zero(
    facade: FacadeSingletonController,
) -> None:
    assert facade.quantidade_entidades_cadastradas() == 0


def test_quantidade_entidades_soma_usuarios_e_produtos(
    facade: FacadeSingletonController,
) -> None:
    gerente = facade.cadastrar_gerente("Ana", "ana@email.com", "anagerente", "Senha123")
    facade.cadastrar_produto("Black Lotus", "carta", 50000.0, 1, gerente.id)
    facade.cadastrar_produto("Booster", "booster", 25.0, 10, gerente.id)

    # 1 usuário + 2 produtos
    assert facade.quantidade_entidades_cadastradas() == 3


def test_facade_diferencia_cliente_de_gerente(
    facade: FacadeSingletonController,
) -> None:
    cliente = facade.cadastrar_usuario("Bruno", "bruno@email.com", "brunocli", "Senha123")
    gerente = facade.cadastrar_gerente("Ana", "ana@email.com", "anagerente", "Senha123")

    assert cliente.perfil == "cliente"
    assert gerente.perfil == "gerente"


def test_facade_orquestra_crud_de_produto(
    facade: FacadeSingletonController,
) -> None:
    gerente = facade.cadastrar_gerente("Ana", "ana@email.com", "anagerente", "Senha123")

    produto = facade.cadastrar_produto("Deck Azul", "deck", 100.0, 5, gerente.id)
    facade.atualizar_produto(produto.id, "Deck Vermelho", "deck", 120.0, 3)
    assert facade.buscar_produto(produto.id).nome == "Deck Vermelho"

    facade.remover_produto(produto.id)
    assert facade.listar_produtos() == []
    # sobra apenas o usuário
    assert facade.quantidade_entidades_cadastradas() == 1
