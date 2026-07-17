import pytest

from app.infra.repositories.repository_factory import (
    ArquivoBinarioRepositoryFactory,
    MemoriaRepositoryFactory,
    RepositoryFactory,
)
from app.infra.repositories.produto_repository import (
    ProdutoArquivoBinarioRepository,
    ProdutoRepository,
)
from app.infra.repositories.usuario_repository import (
    UsuarioArquivoBinarioRepository,
    UsuarioRepository,
)


@pytest.mark.parametrize(
    "tipo_persistencia, fabrica_esperada",
    [
        ("memoria", MemoriaRepositoryFactory),
        ("invalido", MemoriaRepositoryFactory),
        ("arquivo", ArquivoBinarioRepositoryFactory),
        ("ARQUIVO", ArquivoBinarioRepositoryFactory),
    ],
)
def test_obter_fabrica_seleciona_fabrica_correta(
    tipo_persistencia: str, fabrica_esperada: type[RepositoryFactory]
) -> None:
    fabrica = RepositoryFactory.obter_fabrica(tipo_persistencia)

    assert isinstance(fabrica, fabrica_esperada)


def test_fabrica_memoria_cria_repositorios_em_memoria() -> None:
    fabrica = MemoriaRepositoryFactory()

    assert isinstance(fabrica.criar_repositorio_usuarios(), UsuarioRepository)
    assert isinstance(fabrica.criar_repositorio_produtos(), ProdutoRepository)


def test_fabrica_arquivo_cria_repositorios_em_arquivo_binario(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    fabrica = ArquivoBinarioRepositoryFactory()

    assert isinstance(fabrica.criar_repositorio_usuarios(), UsuarioArquivoBinarioRepository)
    assert isinstance(fabrica.criar_repositorio_produtos(), ProdutoArquivoBinarioRepository)


def test_obter_fabrica_usa_variavel_de_ambiente_por_padrao(monkeypatch) -> None:
    monkeypatch.setenv("WIZARDRY_PERSISTENCIA", "arquivo")

    fabrica = RepositoryFactory.obter_fabrica()

    assert isinstance(fabrica, ArquivoBinarioRepositoryFactory)
