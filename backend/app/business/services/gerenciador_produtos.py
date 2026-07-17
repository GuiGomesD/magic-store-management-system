from app.domain.excecoes import (
    DadosInvalidosError,
    ProdutoNaoEncontradoError,
    UsuarioNaoEncontradoError,
)
from app.domain.produto import Produto
from app.domain.usuario import PERFIL_GERENTE
from backend.app.infra.repositories.produto_repository import ProdutoRepository
from backend.app.infra.repositories.usuario_repository import UsuarioRepository

TIPOS_PERMITIDOS = frozenset({"carta", "booster", "deck", "acessorio"})


class GerenciadorProdutos:
    """Camada de controle do CRUD de Produto (usado pelo Gerente)."""

    def __init__(
        self,
        repositorio: ProdutoRepository,
        repositorio_usuarios: UsuarioRepository,
    ) -> None:
        self._repositorio = repositorio
        self._repositorio_usuarios = repositorio_usuarios

    def adicionar_produto(
        self,
        nome: str,
        tipo: str,
        preco: float,
        quantidade_estoque: int,
        gerente_id: int,
    ) -> Produto:
        nome_tratado = nome.strip()
        tipo_tratado = tipo.strip().lower()

        self._validar_nome(nome_tratado)
        self._validar_tipo(tipo_tratado)
        self._validar_preco(preco)
        self._validar_estoque(quantidade_estoque)
        self._validar_gerente(gerente_id)

        produto = Produto(
            id=self._repositorio.gerar_proximo_id(),
            nome=nome_tratado,
            tipo=tipo_tratado,
            preco=preco,
            quantidade_estoque=quantidade_estoque,
            gerente_id=gerente_id,
        )
        return self._repositorio.salvar(produto)

    def listar_produtos(self) -> list[Produto]:
        return self._repositorio.buscar_todos()

    def buscar_produto(self, id: int) -> Produto:
        produto = self._repositorio.buscar_por_id(id)
        if produto is None:
            raise ProdutoNaoEncontradoError("Produto não encontrado")
        return produto

    def atualizar_produto(
        self,
        id: int,
        nome: str,
        tipo: str,
        preco: float,
        quantidade_estoque: int,
    ) -> Produto:
        produto = self.buscar_produto(id)

        nome_tratado = nome.strip()
        tipo_tratado = tipo.strip().lower()

        self._validar_nome(nome_tratado)
        self._validar_tipo(tipo_tratado)
        self._validar_preco(preco)
        self._validar_estoque(quantidade_estoque)

        produto.nome = nome_tratado
        produto.tipo = tipo_tratado
        produto.preco = preco
        produto.quantidade_estoque = quantidade_estoque
        return self._repositorio.salvar(produto)

    def remover_produto(self, id: int) -> None:
        if not self._repositorio.remover(id):
            raise ProdutoNaoEncontradoError("Produto não encontrado")

    def contar_produtos(self) -> int:
        return self._repositorio.contar()

    def _validar_nome(self, nome: str) -> None:
        if not nome:
            raise DadosInvalidosError("Nome do produto não pode ser vazio")

    def _validar_tipo(self, tipo: str) -> None:
        if tipo not in TIPOS_PERMITIDOS:
            raise DadosInvalidosError(
                "Tipo inválido. Use: carta, booster, deck ou acessorio"
            )

    def _validar_preco(self, preco: float) -> None:
        if preco <= 0:
            raise DadosInvalidosError("Preço deve ser maior que zero")

    def _validar_estoque(self, quantidade_estoque: int) -> None:
        if quantidade_estoque < 0:
            raise DadosInvalidosError("Quantidade em estoque não pode ser negativa")

    def _validar_gerente(self, gerente_id: int) -> None:
        gerente = self._repositorio_usuarios.buscar_por_id(gerente_id)
        if gerente is None:
            raise UsuarioNaoEncontradoError(
                "Gerente responsável pelo produto não existe"
            )
        if gerente.perfil != PERFIL_GERENTE:
            raise DadosInvalidosError(
                "Somente usuários com perfil de gerente podem cadastrar produtos"
            )
