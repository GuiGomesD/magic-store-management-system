from fastapi import APIRouter, Depends, HTTPException, status

from app.api.router import obter_facade
from app.api.schemas import (
    ProdutoAtualizacao,
    ProdutoCriacao,
    ProdutoResposta,
    QuantidadeEntidadesResposta,
)
from app.domain.excecoes import (
    DadosInvalidosError,
    PersistenciaError,
    ProdutoNaoEncontradoError,
    UsuarioNaoEncontradoError,
)
from app.domain.produto import Produto
from app.business.services.facade_controller import FacadeSingletonController

router = APIRouter(prefix="/produtos", tags=["produtos"])


def converter_para_resposta(produto: Produto) -> ProdutoResposta:
    return ProdutoResposta(
        id=produto.id,
        nome=produto.nome,
        tipo=produto.tipo,
        preco=produto.preco,
        quantidade_estoque=produto.quantidade_estoque,
        gerente_id=produto.gerente_id,
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ProdutoResposta)
def criar_produto(
    dados: ProdutoCriacao,
    facade: FacadeSingletonController = Depends(obter_facade),
) -> ProdutoResposta:
    try:
        produto = facade.cadastrar_produto(
            dados.nome,
            dados.tipo,
            dados.preco,
            dados.quantidade_estoque,
            dados.gerente_id,
        )
    except DadosInvalidosError as erro:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(erro)) from erro
    except UsuarioNaoEncontradoError as erro:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
    except PersistenciaError as erro:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(erro)
        ) from erro

    return converter_para_resposta(produto)


@router.get("", response_model=list[ProdutoResposta])
def listar_produtos(
    facade: FacadeSingletonController = Depends(obter_facade),
) -> list[ProdutoResposta]:
    return [converter_para_resposta(produto) for produto in facade.listar_produtos()]


@router.get("/quantidade", response_model=QuantidadeEntidadesResposta)
def contar_entidades(
    facade: FacadeSingletonController = Depends(obter_facade),
) -> QuantidadeEntidadesResposta:
    return QuantidadeEntidadesResposta(
        quantidade=facade.quantidade_entidades_cadastradas()
    )


@router.get("/{produto_id}", response_model=ProdutoResposta)
def buscar_produto(
    produto_id: int,
    facade: FacadeSingletonController = Depends(obter_facade),
) -> ProdutoResposta:
    try:
        produto = facade.buscar_produto(produto_id)
    except ProdutoNaoEncontradoError as erro:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro

    return converter_para_resposta(produto)


@router.put("/{produto_id}", response_model=ProdutoResposta)
def atualizar_produto(
    produto_id: int,
    dados: ProdutoAtualizacao,
    facade: FacadeSingletonController = Depends(obter_facade),
) -> ProdutoResposta:
    try:
        produto = facade.atualizar_produto(
            produto_id,
            dados.nome,
            dados.tipo,
            dados.preco,
            dados.quantidade_estoque,
        )
    except DadosInvalidosError as erro:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=str(erro)) from erro
    except ProdutoNaoEncontradoError as erro:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
    except PersistenciaError as erro:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(erro)
        ) from erro

    return converter_para_resposta(produto)


@router.delete("/{produto_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(
    produto_id: int,
    facade: FacadeSingletonController = Depends(obter_facade),
) -> None:
    try:
        facade.remover_produto(produto_id)
    except ProdutoNaoEncontradoError as erro:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(erro)) from erro
    except PersistenciaError as erro:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(erro)
        ) from erro
