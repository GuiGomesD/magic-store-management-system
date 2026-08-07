from app.business.observers.produto_observer import ProdutoObserver
from app.business.interfaces.logger_interface import LoggerInterface
from app.domain.produto import Produto


class LoggerObserver(ProdutoObserver):

    def __init__(self, logger: LoggerInterface):
        self._logger = logger

    def produto_cadastrado(self, produto: Produto):
        self._logger.info(f"Produto {produto.id} cadastrado")

    def produto_atualizado(self, produto: Produto):
        self._logger.info(f"Produto {produto.id} atualizado")

    def produto_removido(self, produto_id: int):
        self._logger.info(f"Produto {produto_id} removido")

    def produto_restaurado(self, produto: Produto):
        self._logger.info(f"Produto {produto.id} restaurado")