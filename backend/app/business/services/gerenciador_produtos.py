from app.domain.excecoes import (
    DadosInvalidosError,
    NadaParaDesfazerError,
    ProdutoNaoEncontradoError,
    UsuarioNaoEncontradoError,
)
from app.domain.produto import Produto
from app.domain.usuario import PERFIL_GERENTE
from app.business.interfaces.logger_interface import LoggerInterface, LoggerNulo
from app.business.interfaces.produto_repository_interface import (
    ProdutoRepositoryInterface,
)
from app.business.mementos.produto_memento import ProdutoMemento

from app.business.interfaces.usuario_repository_interface import (
    UsuarioRepositoryInterface,
)

from app.business.strategy.atualizacao_completa_strategy import AtualizacaoCompletaStrategy

TIPOS_PERMITIDOS = frozenset({"carta", "booster", "deck", "acessorio"})


class GerenciadorProdutos:
    """Camada de controle do CRUD de Produto (usado pelo Gerente).

    Também atua como Caretaker do padrão Memento: antes de aplicar uma
    atualização, guarda uma "fotografia" (`ProdutoMemento`) do estado
    anterior do produto, permitindo desfazer somente a última
    atualização realizada em cada produto.
    """

    def __init__(
        self,
        repositorio: ProdutoRepositoryInterface,
        repositorio_usuarios: UsuarioRepositoryInterface,
        logger: LoggerInterface | None = None,
    ) -> None:
        self._repositorio = repositorio
        self._repositorio_usuarios = repositorio_usuarios
        self._logger = logger or LoggerNulo()
        self._mementos_atualizacao: dict[int, ProdutoMemento] = {}
        self._update_strategy = AtualizacaoCompletaStrategy()

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
        produto_salvo = self._repositorio.salvar(produto)
        self._logger.info(f"Produto '{nome_tratado}' cadastrado pelo gerente {gerente_id}")
        return produto_salvo

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

        self._mementos_atualizacao[id] = ProdutoMemento.criar(produto)

        self._update_strategy.atualizar(
            produto,
            nome_tratado,
            tipo_tratado,
            preco,
            quantidade_estoque,
        )
        produto_atualizado = self._repositorio.salvar(produto)
        self._logger.info(f"Produto {id} atualizado")
        return produto_atualizado

    def desfazer_atualizacao_produto(self, id: int) -> Produto:
        memento = self._mementos_atualizacao.get(id)
        if memento is None:
            if self._repositorio.buscar_por_id(id) is None:
                raise ProdutoNaoEncontradoError("Produto não encontrado")
            raise NadaParaDesfazerError(
                "Não há atualização anterior para desfazer neste produto"
            )

        produto_restaurado = memento.restaurar()
        produto_salvo = self._repositorio.salvar(produto_restaurado)
        del self._mementos_atualizacao[id]
        self._logger.info(f"Última atualização do produto {id} desfeita")
        return produto_salvo

    def remover_produto(self, id: int) -> None:
        if not self._repositorio.remover(id):
            self._logger.erro(f"Tentativa de remover produto inexistente: {id}")
            raise ProdutoNaoEncontradoError("Produto não encontrado")
        self._mementos_atualizacao.pop(id, None)
        self._logger.info(f"Produto {id} removido")

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