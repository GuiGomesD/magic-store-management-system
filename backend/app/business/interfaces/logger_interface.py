from abc import ABC, abstractmethod


class LoggerInterface(ABC):
    """Contrato de log que a camada business espera, independente da
    biblioteca de log usada por trás (ver padrão Adapter em infra/logging).
    """

    @abstractmethod
    def info(self, mensagem: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def erro(self, mensagem: str) -> None:
        raise NotImplementedError


class LoggerNulo(LoggerInterface):
    """Null Object: usado quando nenhum logger é injetado, para que a
    camada business nunca precise depender de um adapter concreto do infra.
    """

    def info(self, mensagem: str) -> None:
        pass

    def erro(self, mensagem: str) -> None:
        pass
