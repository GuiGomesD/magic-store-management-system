import os
from abc import ABC, abstractmethod

from app.business.interfaces.produto_repository_interface import (
    ProdutoRepositoryInterface,
)
from app.business.interfaces.usuario_repository_interface import (
    UsuarioRepositoryInterface,
)
from app.infra.repositories.produto_repository import (
    ProdutoArquivoBinarioRepository,
    ProdutoRepository,
)
from app.infra.repositories.usuario_repository import (
    UsuarioArquivoBinarioRepository,
    UsuarioRepository,
)

PERSISTENCIA_MEMORIA = "memoria"
PERSISTENCIA_ARQUIVO = "arquivo"


class RepositoryFactory(ABC):
    """Abstract Factory: cria a família de repositórios de uma mesma
    estratégia de persistência (todos em memória ou todos em arquivo),
    para que a camada business nunca dependa das classes concretas do infra.
    """

    @abstractmethod
    def criar_repositorio_usuarios(self) -> UsuarioRepositoryInterface:
        raise NotImplementedError

    @abstractmethod
    def criar_repositorio_produtos(self) -> ProdutoRepositoryInterface:
        raise NotImplementedError

    @staticmethod
    def obter_fabrica(tipo_persistencia: str | None = None) -> "RepositoryFactory":
        """Factory Method: seleciona a fábrica concreta a partir do tipo de
        persistência configurado (padrão: variável de ambiente
        WIZARDRY_PERSISTENCIA).
        """
        tipo = (tipo_persistencia or os.getenv("WIZARDRY_PERSISTENCIA", PERSISTENCIA_MEMORIA)).lower()
        if tipo == PERSISTENCIA_ARQUIVO:
            return ArquivoBinarioRepositoryFactory()
        return MemoriaRepositoryFactory()


class MemoriaRepositoryFactory(RepositoryFactory):
    """Cria repositórios que mantêm os dados apenas em memória RAM."""

    def criar_repositorio_usuarios(self) -> UsuarioRepositoryInterface:
        return UsuarioRepository()

    def criar_repositorio_produtos(self) -> ProdutoRepositoryInterface:
        return ProdutoRepository()


class ArquivoBinarioRepositoryFactory(RepositoryFactory):
    """Cria repositórios que persistem os dados em arquivo binário (pickle)."""

    def criar_repositorio_usuarios(self) -> UsuarioRepositoryInterface:
        return UsuarioArquivoBinarioRepository()

    def criar_repositorio_produtos(self) -> ProdutoRepositoryInterface:
        return ProdutoArquivoBinarioRepository()
