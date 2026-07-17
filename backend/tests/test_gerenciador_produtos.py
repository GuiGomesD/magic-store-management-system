import pytest

from app.domain.excecoes import (
    DadosInvalidosError,
    ProdutoNaoEncontradoError,
    UsuarioNaoEncontradoError,
)
from backend.app.infra.repositories.produto_repository import (
    ProdutoArquivoBinarioRepository,
    ProdutoRepository,
)
from app.domain.usuario import PERFIL_GERENTE
from backend.app.infra.repositories.usuario_repository import UsuarioRepository
from backend.app.business.services.gerenciador_produtos import GerenciadorProdutos
from backend.app.business.services.gerenciador_usuarios import GerenciadorUsuarios


@pytest.fixture
def repositorio_usuarios() -> UsuarioRepository:
    return UsuarioRepository()


@pytest.fixture
def gerente_id(repositorio_usuarios: UsuarioRepository) -> int:
    gerenciador_usuarios = GerenciadorUsuarios(repositorio_usuarios)
    gerente = gerenciador_usuarios.adicionar_usuario(
        "Ana Gerente", "ana@email.com", "anagerente", "Senha123", PERFIL_GERENTE
    )
    return gerente.id


@pytest.fixture
def gerenciador(repositorio_usuarios: UsuarioRepository) -> GerenciadorProdutos:
    return GerenciadorProdutos(ProdutoRepository(), repositorio_usuarios)


def test_deve_retornar_lista_vazia_quando_nao_houver_produtos(
    gerenciador: GerenciadorProdutos,
) -> None:
    assert gerenciador.listar_produtos() == []


def test_deve_adicionar_produto_com_sucesso(
    gerenciador: GerenciadorProdutos, gerente_id: int
) -> None:
    produto = gerenciador.adicionar_produto("Black Lotus", "Carta", 50000.0, 1, gerente_id)

    produtos = gerenciador.listar_produtos()

    assert len(produtos) == 1
    assert produtos[0].id == produto.id
    assert produtos[0].nome == "Black Lotus"
    assert produtos[0].tipo == "carta"
    assert produtos[0].preco == 50000.0
    assert produtos[0].quantidade_estoque == 1
    assert produtos[0].gerente_id == gerente_id


def test_deve_rejeitar_produto_de_gerente_inexistente(
    gerenciador: GerenciadorProdutos,
) -> None:
    with pytest.raises(UsuarioNaoEncontradoError):
        gerenciador.adicionar_produto("Booster", "booster", 25.0, 10, 999)


def test_deve_rejeitar_produto_cadastrado_por_cliente(
    gerenciador: GerenciadorProdutos, repositorio_usuarios: UsuarioRepository
) -> None:
    gerenciador_usuarios = GerenciadorUsuarios(repositorio_usuarios)
    cliente = gerenciador_usuarios.adicionar_usuario(
        "Bruno Cliente", "bruno@email.com", "brunocli", "Senha123"
    )

    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_produto("Booster", "booster", 25.0, 10, cliente.id)


def test_deve_rejeitar_produto_com_nome_vazio(
    gerenciador: GerenciadorProdutos, gerente_id: int
) -> None:
    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_produto("   ", "carta", 10.0, 1, gerente_id)


def test_deve_rejeitar_produto_com_tipo_invalido(
    gerenciador: GerenciadorProdutos, gerente_id: int
) -> None:
    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_produto("Item", "invalido", 10.0, 1, gerente_id)


def test_deve_rejeitar_produto_com_preco_nao_positivo(
    gerenciador: GerenciadorProdutos, gerente_id: int
) -> None:
    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_produto("Item", "carta", 0.0, 1, gerente_id)


def test_deve_rejeitar_produto_com_estoque_negativo(
    gerenciador: GerenciadorProdutos, gerente_id: int
) -> None:
    with pytest.raises(DadosInvalidosError):
        gerenciador.adicionar_produto("Item", "carta", 10.0, -1, gerente_id)


def test_deve_buscar_produto_por_id(
    gerenciador: GerenciadorProdutos, gerente_id: int
) -> None:
    produto = gerenciador.adicionar_produto("Deck Azul", "deck", 100.0, 5, gerente_id)

    encontrado = gerenciador.buscar_produto(produto.id)

    assert encontrado.id == produto.id


def test_deve_lancar_erro_ao_buscar_produto_inexistente(
    gerenciador: GerenciadorProdutos,
) -> None:
    with pytest.raises(ProdutoNaoEncontradoError):
        gerenciador.buscar_produto(999)


def test_deve_atualizar_produto(
    gerenciador: GerenciadorProdutos, gerente_id: int
) -> None:
    produto = gerenciador.adicionar_produto("Deck Azul", "deck", 100.0, 5, gerente_id)

    atualizado = gerenciador.atualizar_produto(produto.id, "Deck Vermelho", "deck", 120.0, 3)

    assert atualizado.nome == "Deck Vermelho"
    assert atualizado.preco == 120.0
    assert atualizado.quantidade_estoque == 3
    assert gerenciador.buscar_produto(produto.id).nome == "Deck Vermelho"


def test_deve_remover_produto(
    gerenciador: GerenciadorProdutos, gerente_id: int
) -> None:
    produto = gerenciador.adicionar_produto("Booster", "booster", 25.0, 10, gerente_id)

    gerenciador.remover_produto(produto.id)

    assert gerenciador.listar_produtos() == []


def test_deve_lancar_erro_ao_remover_produto_inexistente(
    gerenciador: GerenciadorProdutos,
) -> None:
    with pytest.raises(ProdutoNaoEncontradoError):
        gerenciador.remover_produto(999)


def test_deve_persistir_produtos_em_arquivo_binario(
    tmp_path, repositorio_usuarios: UsuarioRepository, gerente_id: int
) -> None:
    caminho_arquivo = tmp_path / "produtos.bin"
    repositorio = ProdutoArquivoBinarioRepository(str(caminho_arquivo))
    gerenciador = GerenciadorProdutos(repositorio, repositorio_usuarios)

    gerenciador.adicionar_produto("Black Lotus", "carta", 50000.0, 1, gerente_id)

    novo_repositorio = ProdutoArquivoBinarioRepository(str(caminho_arquivo))
    novo_gerenciador = GerenciadorProdutos(novo_repositorio, repositorio_usuarios)

    produtos = novo_gerenciador.listar_produtos()

    assert len(produtos) == 1
    assert produtos[0].nome == "Black Lotus"
