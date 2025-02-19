from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.database import get_session
from app.models.ingrediente import Ingrediente

router = APIRouter(prefix="/ingredientes", tags=["Ingredientes"])

@router.get("/", response_model=List[Ingrediente], tags=["Ingredientes"])
def listar_ingredientes(session: Session = Depends(get_session)):
    try:
        ingredientes = session.exec(select(Ingrediente)).all()
        return ingredientes
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar ingredientes"
        ) from e

@router.post("/", response_model=Ingrediente)
def criar_ingrediente(ingrediente: Ingrediente, session: Session = Depends(get_session)):
    try:
        session.add(ingrediente)
        session.commit()
        session.refresh(ingrediente)
        return ingrediente
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar ingrediente"
        ) from e

@router.get("/{ingrediente_id}", response_model=Ingrediente, tags=["Ingredientes"])
def obter_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    try:
        ingrediente = session.get(Ingrediente, ingrediente_id)
        if not ingrediente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingrediente não encontrado"
            )
        return ingrediente
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter ingrediente"
        ) from e

@router.put("/{ingrediente_id}", response_model=Ingrediente, tags=["Ingredientes"])
def atualizar_ingrediente(ingrediente_id: int, ingrediente: Ingrediente, session: Session = Depends(get_session)):
    try:
        ingrediente_existente = session.get(Ingrediente, ingrediente_id)
        if not ingrediente_existente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingrediente não encontrado"
            )

        # Atualizar os campos do ingrediente existente
        ingrediente_existente.nome = ingrediente.nome
        ingrediente_existente.quantidade = ingrediente.quantidade
        ingrediente_existente.unidade_medida = ingrediente.unidade_medida

        session.commit()
        session.refresh(ingrediente_existente)
        return ingrediente_existente
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar ingrediente"
        ) from e

@router.delete("/{ingrediente_id}", tags=["Ingredientes"])
def deletar_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    try:
        ingrediente = session.get(Ingrediente, ingrediente_id)
        if not ingrediente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingrediente não encontrado"
            )
        session.delete(ingrediente)
        session.commit()
        return {"message": "Ingrediente deletado com sucesso"}
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar ingrediente"
        ) from e
