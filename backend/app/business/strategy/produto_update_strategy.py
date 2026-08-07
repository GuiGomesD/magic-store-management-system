from abc import ABC, abstractmethod

from app.domain.produto import Produto


class ProdutoUpdateStrategy(ABC):

    @abstractmethod
    def atualizar(
        self,
        produto: Produto,
        nome: str,
        tipo: str,
        preco: float,
        quantidade_estoque: int,
    ) -> None:
        pass