import os

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas import UsuarioCriacao, UsuarioLogin, UsuarioResposta
from app.domain.excecoes import (
    CredenciaisInvalidasError,
    DadosInvalidosError,
    EmailDuplicadoError,
    LoginDuplicadoError,
    PersistenciaError,
)
from app.domain.usuario import Usuario
from app.repository.usuario_repository import (
    UsuarioArquivoBinarioRepository,
    UsuarioRepository,
)
from app.service.gerenciador_usuarios import GerenciadorUsuarios


def criar_repositorio() -> UsuarioRepository:
    tipo_persistencia = os.getenv("WIZARDRY_PERSISTENCIA", "memoria").lower()

    if tipo_persistencia == "arquivo":
        return UsuarioArquivoBinarioRepository()

    return UsuarioRepository()


repositorio_compartilhado = criar_repositorio()
gerenciador_compartilhado = GerenciadorUsuarios(repositorio_compartilhado)

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def obter_gerenciador() -> GerenciadorUsuarios:
    return gerenciador_compartilhado


def converter_para_resposta(usuario: Usuario) -> UsuarioResposta:
    return UsuarioResposta(
        id=usuario.id,
        nome=usuario.nome,
        email=usuario.email,
        login=usuario.login,
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UsuarioResposta)
def criar_usuario(
    dados: UsuarioCriacao,
    gerenciador: GerenciadorUsuarios = Depends(obter_gerenciador),
) -> UsuarioResposta:
    try:
        usuario = gerenciador.adicionar_usuario(
            dados.nome,
            dados.email,
            dados.login,
            dados.senha,
        )
    except DadosInvalidosError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(erro),
        ) from erro
    except (EmailDuplicadoError, LoginDuplicadoError) as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro),
        ) from erro
    except PersistenciaError as erro:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(erro),
        ) from erro

    return converter_para_resposta(usuario)


@router.post("/login", response_model=UsuarioResposta)
def autenticar_usuario(
    dados: UsuarioLogin,
    gerenciador: GerenciadorUsuarios = Depends(obter_gerenciador),
) -> UsuarioResposta:
    try:
        usuario = gerenciador.autenticar_usuario(dados.login, dados.senha)
    except CredenciaisInvalidasError as erro:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(erro),
        ) from erro
    except PersistenciaError as erro:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(erro),
        ) from erro

    return converter_para_resposta(usuario)


@router.get("", response_model=list[UsuarioResposta])
def listar_usuarios(
    gerenciador: GerenciadorUsuarios = Depends(obter_gerenciador),
) -> list[UsuarioResposta]:
    usuarios = gerenciador.listar_usuarios()
    return [converter_para_resposta(usuario) for usuario in usuarios]
