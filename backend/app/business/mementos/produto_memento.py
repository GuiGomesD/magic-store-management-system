from __future__ import annotations

from dataclasses import dataclass

from app.domain.produto import Produto


@dataclass(frozen=True)
class ProdutoMemento:

    produto_id: int
    nome: str
    tipo: str
    preco: float
    quantidade_estoque: int
    gerente_id: int

    @staticmethod
    def criar(produto: Produto) -> ProdutoMemento:
        return ProdutoMemento(
            produto_id=produto.id,
            nome=produto.nome,
            tipo=produto.tipo,
            preco=produto.preco,
            quantidade_estoque=produto.quantidade_estoque,
            gerente_id=produto.gerente_id,
        )

    def restaurar(self) -> Produto:
        return Produto(
            id=self.produto_id,
            nome=self.nome,
            tipo=self.tipo,
            preco=self.preco,
            quantidade_estoque=self.quantidade_estoque,
            gerente_id=self.gerente_id,
        )