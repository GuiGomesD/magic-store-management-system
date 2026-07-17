from app.business.interfaces.registro_acesso_repository_interface import (
    RegistroAcessoRepositoryInterface,
)
from app.domain.registro_acesso import RegistroAcesso

ID_INICIAL = 1


class RegistroAcessoRepository(RegistroAcessoRepositoryInterface):
    """Repositório em memória RAM dos acessos (logins) realizados."""

    def __init__(self) -> None:
        self._registros: dict[int, RegistroAcesso] = {}
        self._proximo_id = ID_INICIAL

    def salvar(self, registro: RegistroAcesso) -> RegistroAcesso:
        self._registros[registro.id] = registro
        return registro

    def buscar_todos(self) -> list[RegistroAcesso]:
        return list(self._registros.values())

    def gerar_proximo_id(self) -> int:
        proximo_id = self._proximo_id
        self._proximo_id += 1
        return proximo_id
