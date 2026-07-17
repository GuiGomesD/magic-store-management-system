from abc import ABC, abstractmethod


class UsuarioRepositoryInterface(ABC):

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def buscar_por_id(self, usuario_id):
        pass

    @abstractmethod
    def salvar(self, usuario):
        pass

    @abstractmethod
    def remover(self, usuario_id):
        pass