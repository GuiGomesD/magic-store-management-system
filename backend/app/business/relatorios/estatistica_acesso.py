from dataclasses import dataclass
from datetime import datetime


@dataclass
class EstatisticaAcessoUsuario:
    usuario_id: int
    nome: str
    login: str
    total_acessos: int
    ultimo_acesso: datetime
