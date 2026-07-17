from abc import ABC, abstractmethod


class ProdutoRepositoryInterface(ABC):

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def buscar_por_id(self, produto_id):
        pass

    @abstractmethod
    def salvar(self, produto):
        pass

    @abstractmethod
    def remover(self, produto_id):
        pass