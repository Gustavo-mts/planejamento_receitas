from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, func
from typing import List
from datetime import date
from app.database import get_session
from app.models.receita import Receita
from app.models.ingrediente import Ingrediente
from app.models.planejamento import Planejamento
from app.models.receita_response import ReceitaResponse
from fastapi import Query
from sqlalchemy.orm import joinedload
from app.models.ingrediente import Ingrediente

router = APIRouter(prefix="/consultas", tags=["Consultas"])


# a) Consultar receita e planejamento por ID
@router.get("/receita/{receita_id}", response_model=Receita, tags=["Consultas"])
def obter_receita_por_id(receita_id: int, session: Session = Depends(get_session)):
    receita = session.exec(
        select(Receita).where(Receita.id == receita_id).options(
            joinedload(Receita.ingredientes),
            joinedload(Receita.planejamentos),
        )
    ).first()
    if not receita:
        raise HTTPException(status_code=404, detail="Receita não encontrada")
    return receita


# b) Listar receitas que contêm um ingrediente específico
@router.get("/receitas/ingrediente/{ingrediente_id}", response_model=List[Receita], tags=["Consultas"])
def listar_receitas_por_ingrediente(ingrediente_id: int, session: Session = Depends(get_session)):
    receitas = session.exec(
        select(Receita).join(Receita.ingredientes).where(Ingrediente.id == ingrediente_id)
    ).all()
    return receitas


# c) Buscar receitas por texto parcial no nome
@router.get("/receitas/busca", response_model=List[Receita], tags=["Consultas"])
def buscar_receitas_por_texto(texto: str, session: Session = Depends(get_session)):
    receitas = session.exec(
        select(Receita).where(Receita.nome.contains(texto)).options(
            joinedload(Receita.ingredientes)  # Eager load para evitar queries adicionais
        )
    ).unique().all()
    return receitas


# d) Filtrar planejamentos por ano
@router.get("/planejamentos/ano/{ano}", response_model=List[Planejamento], tags=["Consultas"])
def listar_planejamentos_por_ano(ano: int, session: Session = Depends(get_session)):
    planejamentos = session.exec(
        select(Planejamento).where(func.strftime("%Y", Planejamento.data) == str(ano)).options(
            joinedload(Planejamento.receita)  # Eager load da receita associada
        )
    ).all()
    return planejamentos


# e) Contar o total de receitas cadastradas
@router.get("/receitas/contagem", tags=["Consultas"])
def contar_receitas(session: Session = Depends(get_session)):
    total_receitas = session.exec(select(func.count(Receita.id))).first()
    return {"total_receitas": total_receitas}


# f) Listar receitas ordenadas por calorias
@router.get("/receitas/ordenadas/calorias", response_model=List[Receita], tags=["Consultas"])
def listar_receitas_ordenadas_calorias(session: Session = Depends(get_session)):
    receitas = session.exec(
        select(Receita).order_by(Receita.calorias.desc()).options(
            joinedload(Receita.ingredientes)
        )
    ).unique().all()
    return receitas


# g) Consultar receitas com múltiplas entidades (ingredientes e planejamentos)
@router.get("/receitas/completo", response_model=List[Receita], tags=["Consultas"])
def listar_todas_receitas_completo(session: Session = Depends(get_session)):
    receitas = session.exec(
        select(Receita).options(
            joinedload(Receita.ingredientes),
            joinedload(Receita.planejamentos)
        )
    ).unique().all()
    return receitas


# h) Contar planejamentos por refeição
@router.get("/planejamentos/contagem/refeicao", tags=["Consultas"])
def contar_planejamentos_por_refeicao(session: Session = Depends(get_session)):
    resultados = session.exec(
        select(Planejamento.refeicao, func.count(Planejamento.id)).group_by(Planejamento.refeicao)
    ).all()
    contagem = [{"refeicao": row[0], "quantidade": row[1]} for row in resultados]
    
    return {"contagem_por_refeicao": contagem}