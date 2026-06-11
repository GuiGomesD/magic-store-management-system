from app.domain.usuario import Usuario

ID_INICIAL = 1


class UsuarioRepository:
    def __init__(self) -> None:
        self._usuarios: dict[int, Usuario] = {}
        self._proximo_id = ID_INICIAL

    def salvar(self, usuario: Usuario) -> Usuario:
        self._usuarios[usuario.id] = usuario
        return usuario

    def buscar_todos(self) -> list[Usuario]:
        return list(self._usuarios.values())

    def existe_email(self, email: str) -> bool:
        email_normalizado = email.strip().lower()
        return any(
            usuario.email.lower() == email_normalizado
            for usuario in self._usuarios.values()
        )

    def gerar_proximo_id(self) -> int:
        proximo_id = self._proximo_id
        self._proximo_id += 1
        return proximo_id
