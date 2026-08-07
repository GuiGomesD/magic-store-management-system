class DadosInvalidosError(Exception):
    pass


class EmailDuplicadoError(Exception):
    pass


class LoginDuplicadoError(Exception):
    pass


class UsuarioNaoEncontradoError(Exception):
    pass


class ProdutoNaoEncontradoError(Exception):
    pass


class CredenciaisInvalidasError(Exception):
    pass


class PersistenciaError(Exception):
    pass


class NadaParaDesfazerError(Exception):
    pass