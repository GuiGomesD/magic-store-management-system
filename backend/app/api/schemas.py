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
