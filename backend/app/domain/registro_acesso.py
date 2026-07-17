from dataclasses import dataclass
from datetime import datetime


@dataclass
class RegistroAcesso:
    id: int
    usuario_id: int
    login: str
    momento: datetime
