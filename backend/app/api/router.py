from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas import UsuarioCriacao, UsuarioResposta
from app.domain.excecoes import DadosInvalidosError, EmailDuplicadoError
from app.domain.usuario import Usuario
from app.repository.usuario_repository import UsuarioRepository
from app.service.gerenciador_usuarios import GerenciadorUsuarios

repositorio_compartilhado = UsuarioRepository()
gerenciador_compartilhado = GerenciadorUsuarios(repositorio_compartilhado)

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def obter_gerenciador() -> GerenciadorUsuarios:
    return gerenciador_compartilhado


def converter_para_resposta(usuario: Usuario) -> UsuarioResposta:
    return UsuarioResposta(id=usuario.id, nome=usuario.nome, email=usuario.email)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UsuarioResposta)
def criar_usuario(
    dados: UsuarioCriacao,
    gerenciador: GerenciadorUsuarios = Depends(obter_gerenciador),
) -> UsuarioResposta:
    try:
        usuario = gerenciador.adicionar_usuario(dados.nome, dados.email)
    except DadosInvalidosError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro
    except EmailDuplicadoError as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro),
        ) from erro

    return converter_para_resposta(usuario)


@router.get("", response_model=list[UsuarioResposta])
def listar_usuarios(
    gerenciador: GerenciadorUsuarios = Depends(obter_gerenciador),
) -> list[UsuarioResposta]:
    usuarios = gerenciador.listar_usuarios()
    return [converter_para_resposta(usuario) for usuario in usuarios]
