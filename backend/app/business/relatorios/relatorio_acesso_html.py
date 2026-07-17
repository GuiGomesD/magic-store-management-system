from html import escape

from app.business.relatorios.estatistica_acesso import EstatisticaAcessoUsuario
from app.business.relatorios.relatorio_acesso import RelatorioAcessoUsuarios

FORMATO_DATA = "%d/%m/%Y %H:%M:%S"


class RelatorioAcessoHTML(RelatorioAcessoUsuarios):
    """Gera o relatório de estatísticas de acesso em HTML."""

    def _montar_cabecalho(self, estatisticas: list[EstatisticaAcessoUsuario]) -> str:
        return (
            "<html><head><meta charset='utf-8'>"
            "<title>Relatório de Acessos de Usuários</title></head><body>"
            "<h1>Relatório de Acessos de Usuários</h1>"
            f"<p>Usuários com acesso registrado: {len(estatisticas)}</p>"
            "<table border='1' cellpadding='4' cellspacing='0'>"
            "<tr><th>Usuário</th><th>Login</th>"
            "<th>Total de acessos</th><th>Último acesso</th></tr>"
        )

    def _montar_corpo(self, estatisticas: list[EstatisticaAcessoUsuario]) -> str:
        if not estatisticas:
            return "<tr><td colspan='4'>Nenhum acesso registrado</td></tr>"

        linhas = []
        for estatistica in estatisticas:
            linhas.append(
                "<tr>"
                f"<td>{escape(estatistica.nome)}</td>"
                f"<td>{escape(estatistica.login)}</td>"
                f"<td>{estatistica.total_acessos}</td>"
                f"<td>{estatistica.ultimo_acesso.strftime(FORMATO_DATA)}</td>"
                "</tr>"
            )
        return "".join(linhas)

    def _montar_rodape(self, estatisticas: list[EstatisticaAcessoUsuario]) -> str:
        return "</table></body></html>"

    def _finalizar(self, cabecalho: str, corpo: str, rodape: str) -> bytes:
        return (cabecalho + corpo + rodape).encode("utf-8")
