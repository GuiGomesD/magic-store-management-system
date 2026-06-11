from pydantic import BaseModel, EmailStr


class UsuarioCriacao(BaseModel):
    nome: str
    email: EmailStr


class UsuarioResposta(BaseModel):
    id: int
    nome: str
    email: str
