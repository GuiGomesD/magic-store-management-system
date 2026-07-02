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
from app.service.facade_controller import FacadeSingletonController

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


def obter_facade() -> FacadeSingletonController:
    return FacadeSingletonController.obter_instancia()


def converter_para_resposta(usuario: Usuario) -> UsuarioResposta:
    return UsuarioResposta(
        id=usuario.id,
        nome=usuario.nome,
        email=usuario.email,
        login=usuario.login,
        perfil=usuario.perfil,
    )


def _cadastrar(cadastrar, dados: UsuarioCriacao) -> UsuarioResposta:
    try:
        usuario = cadastrar(dados.nome, dados.email, dados.login, dados.senha)
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


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UsuarioResposta)
def criar_usuario(
    dados: UsuarioCriacao,
    facade: FacadeSingletonController = Depends(obter_facade),
) -> UsuarioResposta:
    return _cadastrar(facade.cadastrar_usuario, dados)


@router.post(
    "/gerentes", status_code=status.HTTP_201_CREATED, response_model=UsuarioResposta
)
def criar_gerente(
    dados: UsuarioCriacao,
    facade: FacadeSingletonController = Depends(obter_facade),
) -> UsuarioResposta:
    return _cadastrar(facade.cadastrar_gerente, dados)


@router.post("/login", response_model=UsuarioResposta)
def autenticar_usuario(
    dados: UsuarioLogin,
    facade: FacadeSingletonController = Depends(obter_facade),
) -> UsuarioResposta:
    try:
        usuario = facade.autenticar_usuario(dados.login, dados.senha)
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
    facade: FacadeSingletonController = Depends(obter_facade),
) -> list[UsuarioResposta]:
    usuarios = facade.listar_usuarios()
    return [converter_para_resposta(usuario) for usuario in usuarios]
