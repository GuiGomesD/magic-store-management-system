from dataclasses import dataclass


@dataclass
class Produto:
    id: int
    nome: str
    tipo: str
    preco: float
    quantidade_estoque: int
    gerente_id: int
