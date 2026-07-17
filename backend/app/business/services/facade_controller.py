from __future__ import annotations

import os

from app.domain.produto import Produto
from app.domain.usuario import PERFIL_CLIENTE, PERFIL_GERENTE, Usuario
from app.infra.repositories.produto_repository import (
    ProdutoArquivoBinarioRepository,
    ProdutoRepository,
)
from app.infra.repositories.usuario_repository import (
    UsuarioArquivoBinarioRepository,
    UsuarioRepository,
)
from app.business.services.gerenciador_produtos import GerenciadorProdutos
from app.business.services.gerenciador_usuarios import GerenciadorUsuarios


def _criar_repositorio_usuarios() -> UsuarioRepository:
    if os.getenv("WIZARDRY_PERSISTENCIA", "memoria").lower() == "arquivo":
        return UsuarioArquivoBinarioRepository()
    return UsuarioRepository()


def _criar_repositorio_produtos() -> ProdutoRepository:
    if os.getenv("WIZARDRY_PERSISTENCIA", "memoria").lower() == "arquivo":
        return ProdutoArquivoBinarioRepository()
    return ProdutoRepository()


class FacadeSingletonController:
    """Fachada única (Facade) e ponto de acesso único (Singleton) do Gerente.

    Concentra os controllers (`GerenciadorUsuarios` e `GerenciadorProdutos`)
    atrás de uma interface única, para que a camada de boundary converse com
    um só objeto. É um Singleton: `obter_instancia()` sempre devolve a mesma
    instância compartilhada por toda a aplicação.
    """

    _instancia: FacadeSingletonController | None = None

    def __new__(cls) -> FacadeSingletonController:
        if cls._instancia is None:
            instancia = super().__new__(cls)
            instancia._inicializar()
            cls._instancia = instancia
        return cls._instancia

    def _inicializar(self) -> None:
        repositorio_usuarios = _criar_repositorio_usuarios()
        repositorio_produtos = _criar_repositorio_produtos()
        self._gerenciador_usuarios = GerenciadorUsuarios(repositorio_usuarios)
        self._gerenciador_produtos = GerenciadorProdutos(
            repositorio_produtos,
            repositorio_usuarios,
        )

    @classmethod
    def obter_instancia(cls) -> FacadeSingletonController:
        return cls()

    @classmethod
    def resetar_instancia(cls) -> None:
        """Descarta o Singleton (útil em testes)."""
        cls._instancia = None

    # ------------------------------------------------------------------
    # Subsistema de Usuários
    # ------------------------------------------------------------------
    def cadastrar_usuario(self, nome: str, email: str, login: str, senha: str) -> Usuario:
        return self._gerenciador_usuarios.adicionar_usuario(
            nome, email, login, senha, PERFIL_CLIENTE
        )

    def cadastrar_gerente(self, nome: str, email: str, login: str, senha: str) -> Usuario:
        return self._gerenciador_usuarios.adicionar_usuario(
            nome, email, login, senha, PERFIL_GERENTE
        )

    def autenticar_usuario(self, login: str, senha: str) -> Usuario:
        return self._gerenciador_usuarios.autenticar_usuario(login, senha)

    def listar_usuarios(self) -> list[Usuario]:
        return self._gerenciador_usuarios.listar_usuarios()

    # ------------------------------------------------------------------
    # Subsistema de Produtos (CRUD gerenciado pelo Gerente)
    # ------------------------------------------------------------------
    def cadastrar_produto(
        self,
        nome: str,
        tipo: str,
        preco: float,
        quantidade_estoque: int,
        gerente_id: int,
    ) -> Produto:
        return self._gerenciador_produtos.adicionar_produto(
            nome, tipo, preco, quantidade_estoque, gerente_id
        )

    def listar_produtos(self) -> list[Produto]:
        return self._gerenciador_produtos.listar_produtos()

    def buscar_produto(self, id: int) -> Produto:
        return self._gerenciador_produtos.buscar_produto(id)

    def atualizar_produto(
        self,
        id: int,
        nome: str,
        tipo: str,
        preco: float,
        quantidade_estoque: int,
    ) -> Produto:
        return self._gerenciador_produtos.atualizar_produto(
            id, nome, tipo, preco, quantidade_estoque
        )

    def remover_produto(self, id: int) -> None:
        self._gerenciador_produtos.remover_produto(id)

    # ------------------------------------------------------------------
    # Estatísticas do sistema
    # ------------------------------------------------------------------
    def quantidade_entidades_cadastradas(self) -> int:
        """Total de entidades cadastradas (usuários + produtos)."""
        return len(self._gerenciador_usuarios.listar_usuarios()) + (
            self._gerenciador_produtos.contar_produtos()
        )
