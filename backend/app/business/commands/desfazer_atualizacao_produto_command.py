from app.business.commands.command import Command


class DesfazerAtualizacaoProdutoCommand(Command):

    def __init__(self, gerenciador, id):
        self.gerenciador = gerenciador
        self.id = id

    def execute(self):
        return self.gerenciador.desfazer_atualizacao_produto(
            self.id
        )