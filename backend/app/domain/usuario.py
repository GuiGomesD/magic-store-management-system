from dataclasses import dataclass


@dataclass
class Usuario:
    id: int
    nome: str
    email: str
    login: str
    senha: str
