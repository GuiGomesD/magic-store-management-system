from app.domain.excecoes import (
    CredenciaisInvalidasError,
    DadosInvalidosError,
    EmailDuplicadoError,
    LoginDuplicadoError,
)
from app.domain.usuario import Usuario
from app.repository.usuario_repository import UsuarioRepository

CARACTERES_ESPECIAIS_AWS = set("!@#$%^&*()_+-=[]{}|'")
TAMANHO_MINIMO_SENHA_AWS = 8
TAMANHO_MAXIMO_SENHA_AWS = 128
TAMANHO_MAXIMO_LOGIN = 12


class GerenciadorUsuarios:
    def __init__(self, repositorio: UsuarioRepository) -> None:
        self._repositorio = repositorio

    def adicionar_usuario(self, nome: str, email: str, login: str, senha: str) -> Usuario:
        nome_tratado = nome.strip()
        email_tratado = email.strip()
        login_tratado = login.strip()

        self._validar_nome(nome_tratado)
        self._validar_email(email_tratado)
        self._validar_login(login_tratado)
        self._validar_senha(senha)

        if self._repositorio.existe_email(email_tratado):
            raise EmailDuplicadoError("E-mail já cadastrado")

        if self._repositorio.existe_login(login_tratado):
            raise LoginDuplicadoError("Login já cadastrado")

        usuario = Usuario(
            id=self._repositorio.gerar_proximo_id(),
            nome=nome_tratado,
            email=email_tratado,
            login=login_tratado,
            senha=senha,
        )
        return self._repositorio.salvar(usuario)

    def autenticar_usuario(self, login: str, senha: str) -> Usuario:
        login_tratado = login.strip()

        if not login_tratado or not senha:
            raise CredenciaisInvalidasError("Login e senha são obrigatórios")

        usuario = self._repositorio.buscar_por_login(login_tratado)
        if usuario is None or usuario.senha != senha:
            raise CredenciaisInvalidasError("Login ou senha inválidos")

        return usuario

    def listar_usuarios(self) -> list[Usuario]:
        return self._repositorio.buscar_todos()

    def _validar_nome(self, nome: str) -> None:
        if not nome:
            raise DadosInvalidosError("Nome não pode ser vazio")

    def _validar_email(self, email: str) -> None:
        if not email or "@" not in email:
            raise DadosInvalidosError("E-mail inválido")

    def _validar_login(self, login: str) -> None:
        if not login:
            raise DadosInvalidosError("Login não pode ser vazio")

        if len(login) > TAMANHO_MAXIMO_LOGIN:
            raise DadosInvalidosError("Login deve ter no máximo 12 caracteres")

        if any(caractere.isdigit() for caractere in login):
            raise DadosInvalidosError("Login não pode conter números")

    def _validar_senha(self, senha: str) -> None:
        if len(senha) < TAMANHO_MINIMO_SENHA_AWS:
            raise DadosInvalidosError("Senha deve ter no mínimo 8 caracteres")

        if len(senha) > TAMANHO_MAXIMO_SENHA_AWS:
            raise DadosInvalidosError("Senha deve ter no máximo 128 caracteres")

        quantidade_grupos = 0
        quantidade_grupos += any(caractere.isupper() for caractere in senha)
        quantidade_grupos += any(caractere.islower() for caractere in senha)
        quantidade_grupos += any(caractere.isdigit() for caractere in senha)
        quantidade_grupos += any(caractere in CARACTERES_ESPECIAIS_AWS for caractere in senha)

        if quantidade_grupos < 3:
            raise DadosInvalidosError(
                "Senha deve conter pelo menos 3 grupos: maiúsculas, minúsculas, números e caracteres especiais"
            )
