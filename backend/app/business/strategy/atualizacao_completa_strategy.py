from app.business.strategy.produto_update_strategy import ProdutoUpdateStrategy
from app.domain.produto import Produto


class AtualizacaoCompletaStrategy(ProdutoUpdateStrategy):

    def atualizar(
        self,
        produto: Produto,
        nome: str,
        tipo: str,
        preco: float,
        quantidade_estoque: int,
    ) -> None:

        produto.nome = nome
        produto.tipo = tipo
        produto.preco = preco
        produto.quantidade_estoque = quantidade_estoque