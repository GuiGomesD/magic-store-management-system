from datetime import datetime

from app.domain.registro_acesso import RegistroAcesso
from app.domain.usuario import Usuario
from app.infra.repositories.registro_acesso_repository import RegistroAcessoRepository
from app.infra.repositories.usuario_repository import UsuarioRepository
from app.business.relatorios.relatorio_acesso_html import RelatorioAcessoHTML
from app.business.relatorios.relatorio_acesso_pdf import RelatorioAcessoPDF


def _preparar_repositorios():
    repositorio_usuarios = UsuarioRepository()
    repositorio_acessos = RegistroAcessoRepository()

    usuario = Usuario(id=1, nome="Ana Silva", email="ana@email.com", login="anasilva", senha="x")
    repositorio_usuarios.salvar(usuario)

    for momento in [datetime(2026, 7, 10, 9, 0), datetime(2026, 7, 15, 18, 30)]:
        repositorio_acessos.salvar(
            RegistroAcesso(
                id=repositorio_acessos.gerar_proximo_id(),
                usuario_id=usuario.id,
                login=usuario.login,
                momento=momento,
            )
        )

    return repositorio_acessos, repositorio_usuarios


def test_relatorio_html_contem_estatisticas_do_usuario() -> None:
    repositorio_acessos, repositorio_usuarios = _preparar_repositorios()

    conteudo = RelatorioAcessoHTML(repositorio_acessos, repositorio_usuarios).gerar()
    html = conteudo.decode("utf-8")

    assert "<html>" in html
    assert "Ana Silva" in html
    assert "anasilva" in html
    assert ">2<" in html  # total de acessos


def test_relatorio_html_sem_acessos_informa_lista_vazia() -> None:
    repositorio_acessos = RegistroAcessoRepository()
    repositorio_usuarios = UsuarioRepository()

    conteudo = RelatorioAcessoHTML(repositorio_acessos, repositorio_usuarios).gerar()

    assert "Nenhum acesso registrado" in conteudo.decode("utf-8")


def test_relatorio_pdf_gera_bytes_com_cabecalho_pdf_valido() -> None:
    repositorio_acessos, repositorio_usuarios = _preparar_repositorios()

    conteudo = RelatorioAcessoPDF(repositorio_acessos, repositorio_usuarios).gerar()

    assert conteudo.startswith(b"%PDF-1.4")
    assert conteudo.rstrip().endswith(b"%%EOF")
    assert b"/Type /Catalog" in conteudo
    assert b"/Type /Page" in conteudo


def test_relatorio_pdf_pagina_quando_ha_muitas_linhas() -> None:
    repositorio_usuarios = UsuarioRepository()
    repositorio_acessos = RegistroAcessoRepository()

    for indice in range(60):
        usuario = Usuario(
            id=indice + 1,
            nome=f"Usuario {indice}",
            email=f"user{indice}@email.com",
            login=f"login{indice}",
            senha="x",
        )
        repositorio_usuarios.salvar(usuario)
        repositorio_acessos.salvar(
            RegistroAcesso(
                id=repositorio_acessos.gerar_proximo_id(),
                usuario_id=usuario.id,
                login=usuario.login,
                momento=datetime(2026, 7, 16, 12, 0),
            )
        )

    conteudo = RelatorioAcessoPDF(repositorio_acessos, repositorio_usuarios).gerar()

    assert conteudo.count(b"/Type /Page /Parent") >= 2
