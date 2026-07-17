import logging

from app.business.interfaces.logger_interface import LoggerInterface

NOME_LOGGER_PADRAO = "magic_store"
FORMATO_PADRAO = "%(asctime)s %(levelname)s %(name)s: %(message)s"


class LoggingLibAdapter(LoggerInterface):
    """Adapter: adequa a API do módulo `logging` da biblioteca padrão do
    Python (métodos `.info()`/`.error()`, configuração de handlers e
    formatters) ao contrato `LoggerInterface` que a camada business
    conhece. Trocar a biblioteca de log no futuro (ex.: loguru) não exige
    alterar nenhum código de business, só criar um novo adapter.
    """

    def __init__(self, nome: str = NOME_LOGGER_PADRAO) -> None:
        self._logger = logging.getLogger(nome)
        if not self._logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(FORMATO_PADRAO))
            self._logger.addHandler(handler)
            self._logger.setLevel(logging.INFO)

    def info(self, mensagem: str) -> None:
        self._logger.info(mensagem)

    def erro(self, mensagem: str) -> None:
        self._logger.error(mensagem)
