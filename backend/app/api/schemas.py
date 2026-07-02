from pydantic import BaseModel, EmailStr


class UsuarioCriacao(BaseModel):
    nome: str
    email: EmailStr
    login: str
    senha: str


class UsuarioLogin(BaseModel):
    login: str
    senha: str


class UsuarioResposta(BaseModel):
    id: int
    nome: str
    email: str
    login: str
    perfil: str


class ProdutoCriacao(BaseModel):
    nome: str
    tipo: str
    preco: float
    quantidade_estoque: int
    gerente_id: int


class ProdutoAtualizacao(BaseModel):
    nome: str
    tipo: str
    preco: float
    quantidade_estoque: int


class ProdutoResposta(BaseModel):
    id: int
    nome: str
    tipo: str
    preco: float
    quantidade_estoque: int
    gerente_id: int


class QuantidadeEntidadesResposta(BaseModel):
    quantidade: int
