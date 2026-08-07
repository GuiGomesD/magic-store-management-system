from __future__ import annotations

from app.domain.produto import Produto
from app.domain.usuario import PERFIL_CLIENTE, PERFIL_GERENTE, Usuario
from app.infra.logging.logging_lib_adapter import LoggingLibAdapter
from app.infra.repositories.repository_factory import RepositoryFactory
from app.business.relatorios.relatorio_acesso_html import RelatorioAcessoHTML
from app.business.relatorios.relatorio_acesso_pdf import RelatorioAcessoPDF
from app.business.services.gerenciador_produtos import GerenciadorProdutos
from app.business.services.gerenciador_usuarios import GerenciadorUsuarios

from app.business.commands.cadastrar_produto_command import CadastrarProdutoCommand
from app.business.commands.atualizar_produto_command import AtualizarProdutoCommand
from app.business.commands.remover_produto_command import RemoverProdutoCommand
from app.business.commands.desfazer_atualizacao_produto_command import (
    DesfazerAtualizacaoProdutoCommand,
)

from app.business.observers.logger_observer import LoggerObserver

FORMATO_RELATORIO_PDF = "pdf"


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
        fabrica = RepositoryFactory.obter_fabrica()
        repositorio_usuarios = fabrica.criar_repositorio_usuarios()
        repositorio_produtos = fabrica.criar_repositorio_produtos()
        repositorio_acessos = fabrica.criar_repositorio_registros_acesso()
        logger = LoggingLibAdapter()
        self._repositorio_usuarios = repositorio_usuarios
        self._repositorio_acessos = repositorio_acessos
        self._gerenciador_usuarios = GerenciadorUsuarios(
            repositorio_usuarios, logger, repositorio_acessos
        )
        self._gerenciador_produtos = GerenciadorProdutos(
            repositorio_produtos,
            repositorio_usuarios,
            logger,
        )

        logger_observer = LoggerObserver(logger)

        self._gerenciador_produtos.adicionar_observer(logger_observer)

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
        command = CadastrarProdutoCommand(
            self._gerenciador_produtos,
            nome,
            tipo,
            preco,
            quantidade_estoque,
            gerente_id,
        )

        return command.execute()

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
        command = AtualizarProdutoCommand(
            self._gerenciador_produtos,
            id,
            nome,
            tipo,
            preco,
            quantidade_estoque,
        )

        return command.execute()

    def remover_produto(self, id: int) -> None:
        command = RemoverProdutoCommand(
        self._gerenciador_produtos,
        id,
        )

        command.execute()

    # ------------------------------------------------------------------
    # Estatísticas do sistema
    # ------------------------------------------------------------------
    def quantidade_entidades_cadastradas(self) -> int:
        """Total de entidades cadastradas (usuários + produtos)."""
        return len(self._gerenciador_usuarios.listar_usuarios()) + (
            self._gerenciador_produtos.contar_produtos()
        )

    def gerar_relatorio_acesso(self, formato: str = "html") -> bytes:
        """Gera o relatório de estatísticas de acesso dos usuários no
        formato pedido ('html' ou 'pdf')."""
        classe_relatorio = (
            RelatorioAcessoPDF
            if formato.strip().lower() == FORMATO_RELATORIO_PDF
            else RelatorioAcessoHTML
        )
        relatorio = classe_relatorio(self._repositorio_acessos, self._repositorio_usuarios)
        return relatorio.gerar()

    def desfazer_atualizacao_produto(self, produto_id: int):
        command = DesfazerAtualizacaoProdutoCommand(
            self._gerenciador_produtos,
            produto_id,
        )

        return command.execute()