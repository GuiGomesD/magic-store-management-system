from dataclasses import dataclass

PERFIL_CLIENTE = "cliente"
PERFIL_GERENTE = "gerente"
PERFIS_PERMITIDOS = frozenset({PERFIL_CLIENTE, PERFIL_GERENTE})


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    login: str
    senha: str
    perfil: str = PERFIL_CLIENTE
