import os
import pickle
from pathlib import Path

from app.domain.excecoes import PersistenciaError
from app.domain.produto import Produto
from app.business.interfaces.produto_repository_interface import (
    ProdutoRepositoryInterface,
)

ID_INICIAL = 1


class ProdutoRepository(ProdutoRepositoryInterface):
    """Repositório em memória RAM."""

    def __init__(self) -> None:
        self._produtos: dict[int, Produto] = {}
        self._proximo_id = ID_INICIAL

    def salvar(self, produto: Produto) -> Produto:
        self._produtos[produto.id] = produto
        return produto

    def buscar_todos(self) -> list[Produto]:
        return list(self._produtos.values())

    def buscar_por_id(self, id: int) -> Produto | None:
        return self._produtos.get(id)

    def remover(self, id: int) -> bool:
        if id not in self._produtos:
            return False
        del self._produtos[id]
        return True

    def contar(self) -> int:
        return len(self._produtos)

    def gerar_proximo_id(self) -> int:
        proximo_id = self._proximo_id
        self._proximo_id += 1
        return proximo_id


class ProdutoArquivoBinarioRepository(ProdutoRepository):
    """Repositório com persistência em arquivo binário usando pickle."""

    def __init__(self, caminho_arquivo: str = "data/produtos.bin") -> None:
        self._caminho_arquivo = Path(caminho_arquivo)
        super().__init__()
        self._carregar_do_arquivo()

    def salvar(self, produto: Produto) -> Produto:
        produto_salvo = super().salvar(produto)
        self._salvar_no_arquivo()
        return produto_salvo

    def remover(self, id: int) -> bool:
        removido = super().remover(id)
        if removido:
            self._salvar_no_arquivo()
        return removido

    def _carregar_do_arquivo(self) -> None:
        if not self._caminho_arquivo.exists():
            return

        try:
            with self._caminho_arquivo.open("rb") as arquivo:
                dados = pickle.load(arquivo)
        except (OSError, pickle.PickleError, EOFError) as erro:
            raise PersistenciaError("Erro ao carregar produtos do arquivo binário") from erro

        self._produtos = dados.get("produtos", {})
        self._proximo_id = dados.get("proximo_id", ID_INICIAL)

    def _salvar_no_arquivo(self) -> None:
        try:
            os.makedirs(self._caminho_arquivo.parent, exist_ok=True)
            with self._caminho_arquivo.open("wb") as arquivo:
                pickle.dump(
                    {
                        "produtos": self._produtos,
                        "proximo_id": self._proximo_id,
                    },
                    arquivo,
                )
        except (OSError, pickle.PickleError) as erro:
            raise PersistenciaError("Erro ao salvar produtos no arquivo binário") from erro
