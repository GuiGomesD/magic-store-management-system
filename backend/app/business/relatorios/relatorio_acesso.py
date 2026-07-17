from abc import ABC, abstractmethod

from app.business.interfaces.registro_acesso_repository_interface import (
    RegistroAcessoRepositoryInterface,
)
from app.business.interfaces.usuario_repository_interface import (
    UsuarioRepositoryInterface,
)
from app.business.relatorios.estatistica_acesso import EstatisticaAcessoUsuario


class RelatorioAcessoUsuarios(ABC):
    """Template Method: fixa o algoritmo de geração do relatório de
    estatísticas de acesso (coletar dados -> cabeçalho -> corpo -> rodapé
    -> finalizar). Cada formato de saída (HTML, PDF, ...) só precisa
    implementar como cada etapa é renderizada.
    """

    def __init__(
        self,
        repositorio_acessos: RegistroAcessoRepositoryInterface,
        repositorio_usuarios: UsuarioRepositoryInterface,
    ) -> None:
        self._repositorio_acessos = repositorio_acessos
        self._repositorio_usuarios = repositorio_usuarios

    def gerar(self) -> bytes:
        estatisticas = self._coletar_estatisticas()
        cabecalho = self._montar_cabecalho(estatisticas)
        corpo = self._montar_corpo(estatisticas)
        rodape = self._montar_rodape(estatisticas)
        return self._finalizar(cabecalho, corpo, rodape)

    def _coletar_estatisticas(self) -> list[EstatisticaAcessoUsuario]:
        usuarios_por_id = {
            usuario.id: usuario for usuario in self._repositorio_usuarios.buscar_todos()
        }

        acessos_por_usuario: dict[int, list] = {}
        for registro in self._repositorio_acessos.buscar_todos():
            acessos_por_usuario.setdefault(registro.usuario_id, []).append(registro.momento)

        estatisticas = []
        for usuario_id, momentos in acessos_por_usuario.items():
            usuario = usuarios_por_id.get(usuario_id)
            if usuario is None:
                continue
            estatisticas.append(
                EstatisticaAcessoUsuario(
                    usuario_id=usuario_id,
                    nome=usuario.nome,
                    login=usuario.login,
                    total_acessos=len(momentos),
                    ultimo_acesso=max(momentos),
                )
            )

        estatisticas.sort(key=lambda estatistica: estatistica.total_acessos, reverse=True)
        return estatisticas

    @abstractmethod
    def _montar_cabecalho(self, estatisticas: list[EstatisticaAcessoUsuario]):
        raise NotImplementedError

    @abstractmethod
    def _montar_corpo(self, estatisticas: list[EstatisticaAcessoUsuario]):
        raise NotImplementedError

    @abstractmethod
    def _montar_rodape(self, estatisticas: list[EstatisticaAcessoUsuario]):
        raise NotImplementedError

    @abstractmethod
    def _finalizar(self, cabecalho, corpo, rodape) -> bytes:
        raise NotImplementedError
