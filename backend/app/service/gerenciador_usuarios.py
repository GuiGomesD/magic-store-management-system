from app.domain.excecoes import DadosInvalidosError, EmailDuplicadoError
from app.domain.usuario import Usuario
from app.repository.usuario_repository import UsuarioRepository


class GerenciadorUsuarios:
    def __init__(self, repositorio: UsuarioRepository) -> None:
        self._repositorio = repositorio

    def adicionar_usuario(self, nome: str, email: str) -> Usuario:
        nome_tratado = nome.strip()
        email_tratado = email.strip()

        if not nome_tratado:
            raise DadosInvalidosError("Nome não pode ser vazio")

        if not email_tratado or "@" not in email_tratado:
            raise DadosInvalidosError("E-mail inválido")

        if self._repositorio.existe_email(email_tratado):
            raise EmailDuplicadoError("E-mail já cadastrado")

        usuario = Usuario(
            id=self._repositorio.gerar_proximo_id(),
            nome=nome_tratado,
            email=email_tratado,
        )
        return self._repositorio.salvar(usuario)

    def listar_usuarios(self) -> list[Usuario]:
        return self._repositorio.buscar_todos()
