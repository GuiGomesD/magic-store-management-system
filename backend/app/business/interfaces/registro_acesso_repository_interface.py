from abc import ABC, abstractmethod

from app.domain.registro_acesso import RegistroAcesso


class RegistroAcessoRepositoryInterface(ABC):

    @abstractmethod
    def gerar_proximo_id(self) -> int:
        pass

    @abstractmethod
    def salvar(self, registro: RegistroAcesso) -> RegistroAcesso:
        pass

    @abstractmethod
    def buscar_todos(self) -> list[RegistroAcesso]:
        pass


class RegistroAcessoRepositoryNulo(RegistroAcessoRepositoryInterface):
    """Null Object: usado quando nenhum repositório de acessos é injetado,
    para que a camada business nunca precise depender de um repositório
    concreto do infra.
    """

    def gerar_proximo_id(self) -> int:
        return 0

    def salvar(self, registro: RegistroAcesso) -> RegistroAcesso:
        return registro

    def buscar_todos(self) -> list[RegistroAcesso]:
        return []
