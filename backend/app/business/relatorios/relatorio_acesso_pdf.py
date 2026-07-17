from app.business.relatorios.estatistica_acesso import EstatisticaAcessoUsuario
from app.business.relatorios.pdf_writer import montar_pdf
from app.business.relatorios.relatorio_acesso import RelatorioAcessoUsuarios

FORMATO_DATA = "%d/%m/%Y %H:%M:%S"


class RelatorioAcessoPDF(RelatorioAcessoUsuarios):
    """Gera o relatório de estatísticas de acesso em PDF."""

    def _montar_cabecalho(self, estatisticas: list[EstatisticaAcessoUsuario]) -> list[str]:
        return [
            "Relatorio de Acessos de Usuarios",
            f"Usuarios com acesso registrado: {len(estatisticas)}",
            "",
            f"{'Usuario':<25}{'Login':<15}{'Acessos':<10}Ultimo acesso",
            "-" * 70,
        ]

    def _montar_corpo(self, estatisticas: list[EstatisticaAcessoUsuario]) -> list[str]:
        if not estatisticas:
            return ["Nenhum acesso registrado"]

        return [
            f"{estatistica.nome[:24]:<25}{estatistica.login[:14]:<15}"
            f"{estatistica.total_acessos:<10}{estatistica.ultimo_acesso.strftime(FORMATO_DATA)}"
            for estatistica in estatisticas
        ]

    def _montar_rodape(self, estatisticas: list[EstatisticaAcessoUsuario]) -> list[str]:
        return []

    def _finalizar(self, cabecalho: list[str], corpo: list[str], rodape: list[str]) -> bytes:
        return montar_pdf([*cabecalho, *corpo, *rodape])
