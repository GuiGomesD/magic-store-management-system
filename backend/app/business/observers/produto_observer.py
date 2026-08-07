from abc import ABC, abstractmethod

from app.domain.produto import Produto


class ProdutoObserver(ABC):

    @abstractmethod
    def produto_cadastrado(self, produto: Produto):
        pass

    @abstractmethod
    def produto_atualizado(self, produto: Produto):
        pass

    @abstractmethod
    def produto_removido(self, produto_id: int):
        pass

    @abstractmethod
    def produto_restaurado(self, produto: Produto):
        pass