import os
import pickle
from pathlib import Path

from app.domain.excecoes import PersistenciaError
from app.domain.usuario import Usuario

ID_INICIAL = 1


class UsuarioRepository:
    """Repositório em memória RAM."""

    def __init__(self) -> None:
        self._usuarios: dict[int, Usuario] = {}
        self._proximo_id = ID_INICIAL

    def salvar(self, usuario: Usuario) -> Usuario:
        self._usuarios[usuario.id] = usuario
        return usuario

    def buscar_todos(self) -> list[Usuario]:
        return list(self._usuarios.values())

    def buscar_por_login(self, login: str) -> Usuario | None:
        login_normalizado = login.strip().lower()
        for usuario in self._usuarios.values():
            if usuario.login.lower() == login_normalizado:
                return usuario
        return None

    def existe_email(self, email: str) -> bool:
        email_normalizado = email.strip().lower()
        return any(
            usuario.email.lower() == email_normalizado
            for usuario in self._usuarios.values()
        )

    def existe_login(self, login: str) -> bool:
        return self.buscar_por_login(login) is not None

    def gerar_proximo_id(self) -> int:
        proximo_id = self._proximo_id
        self._proximo_id += 1
        return proximo_id


class UsuarioArquivoBinarioRepository(UsuarioRepository):
    """Repositório com persistência em arquivo binário usando pickle."""

    def __init__(self, caminho_arquivo: str = "data/usuarios.bin") -> None:
        self._caminho_arquivo = Path(caminho_arquivo)
        super().__init__()
        self._carregar_do_arquivo()

    def salvar(self, usuario: Usuario) -> Usuario:
        usuario_salvo = super().salvar(usuario)
        self._salvar_no_arquivo()
        return usuario_salvo

    def _carregar_do_arquivo(self) -> None:
        if not self._caminho_arquivo.exists():
            return

        try:
            with self._caminho_arquivo.open("rb") as arquivo:
                dados = pickle.load(arquivo)
        except (OSError, pickle.PickleError, EOFError) as erro:
            raise PersistenciaError("Erro ao carregar usuários do arquivo binário") from erro

        self._usuarios = dados.get("usuarios", {})
        self._proximo_id = dados.get("proximo_id", ID_INICIAL)

    def _salvar_no_arquivo(self) -> None:
        try:
            os.makedirs(self._caminho_arquivo.parent, exist_ok=True)
            with self._caminho_arquivo.open("wb") as arquivo:
                pickle.dump(
                    {
                        "usuarios": self._usuarios,
                        "proximo_id": self._proximo_id,
                    },
                    arquivo,
                )
        except (OSError, pickle.PickleError) as erro:
            raise PersistenciaError("Erro ao salvar usuários no arquivo binário") from erro
