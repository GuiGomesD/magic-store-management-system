from app.business.commands.command import Command


class RemoverProdutoCommand(Command):

    def __init__(self, gerenciador, id):
        self.gerenciador = gerenciador
        self.id = id

    def execute(self):
        return self.gerenciador.remover_produto(self.id)