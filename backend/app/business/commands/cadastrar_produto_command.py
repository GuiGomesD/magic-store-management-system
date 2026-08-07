from app.business.commands.command import Command


class CadastrarProdutoCommand(Command):

    def __init__(
        self,
        gerenciador,
        nome,
        tipo,
        preco,
        quantidade_estoque,
        gerente_id,
    ):
        self.gerenciador = gerenciador
        self.nome = nome
        self.tipo = tipo
        self.preco = preco
        self.quantidade = quantidade_estoque
        self.gerente = gerente_id

    def execute(self):
        return self.gerenciador.adicionar_produto(
            self.nome,
            self.tipo,
            self.preco,
            self.quantidade,
            self.gerente,
        )