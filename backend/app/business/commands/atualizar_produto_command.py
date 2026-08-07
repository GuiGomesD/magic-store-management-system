from app.business.commands.command import Command


class AtualizarProdutoCommand(Command):

    def __init__(
        self,
        gerenciador,
        id,
        nome,
        tipo,
        preco,
        quantidade,
    ):
        self.gerenciador = gerenciador
        self.id = id
        self.nome = nome
        self.tipo = tipo
        self.preco = preco
        self.quantidade = quantidade

    def execute(self):
        return self.gerenciador.atualizar_produto(
            self.id,
            self.nome,
            self.tipo,
            self.preco,
            self.quantidade,
        )