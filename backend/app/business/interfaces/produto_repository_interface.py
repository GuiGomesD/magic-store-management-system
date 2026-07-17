from abc import ABC, abstractmethod
from app.domain.produto import Produto


class ProdutoRepositoryInterface(ABC):

    @abstractmethod
    def gerar_proximo_id(self) -> int:
        pass

    @abstractmethod
    def salvar(self, produto: Produto) -> Produto:
        pass

    @abstractmethod
    def buscar_todos(self) -> list[Produto]:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> Produto | None:
        pass

    @abstractmethod
    def remover(self, id: int) -> bool:
        pass

    @abstractmethod
    def contar(self) -> int:
        pass