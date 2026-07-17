from abc import ABC, abstractmethod

from app.domain.usuario import Usuario


class UsuarioRepositoryInterface(ABC):

    @abstractmethod
    def salvar(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def buscar_todos(self) -> list[Usuario]:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> Usuario | None:
        pass

    @abstractmethod
    def buscar_por_login(self, login: str) -> Usuario | None:
        pass

    @abstractmethod
    def existe_email(self, email: str) -> bool:
        pass

    @abstractmethod
    def existe_login(self, login: str) -> bool:
        pass

    @abstractmethod
    def gerar_proximo_id(self) -> int:
        pass