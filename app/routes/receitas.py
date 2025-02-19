from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.database import db
from app.models.receita import Receita
from bson import ObjectId

router = APIRouter(prefix="/receitas", tags=["Receitas"])

# 🚀 Rota para listar todas as receitas
@router.get("/", response_model=List[Receita])
async def listar_receitas():
    try:
        receitas_cursor = db.receitas.find()
        receitas = await receitas_cursor.to_list(100)
        for receita in receitas:
            receita["_id"] = str(receita["_id"])  # Converter ObjectId para string
        return receitas
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar receitas: {str(e)}"
        )

# 🚀 Rota para criar uma nova receita
@router.post("/", response_model=Receita)
async def criar_receita(receita: Receita):
    try:
        receita_dict = receita.dict()
        result = await db.receitas.insert_one(receita_dict)
        receita_dict["_id"] = str(result.inserted_id)
        return receita_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar receita: {str(e)}"
        )

# 🚀 Rota para obter uma receita específica por ID
@router.get("/{receita_id}", response_model=Receita)
async def obter_receita(receita_id: str):
    try:
        receita = await db.receitas.find_one({"_id": ObjectId(receita_id)})
        if not receita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receita não encontrada"
            )
        receita["_id"] = str(receita["_id"])
        return receita
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter receita: {str(e)}"
        )

# 🚀 Rota para atualizar uma receita por ID
@router.put("/{receita_id}", response_model=Receita)
async def atualizar_receita(receita_id: str, receita: Receita):
    try:
        receita_dict = receita.dict(exclude_unset=True)
        result = await db.receitas.update_one(
            {"_id": ObjectId(receita_id)}, {"$set": receita_dict}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receita não encontrada ou sem mudanças"
            )

        receita_dict["_id"] = receita_id
        return receita_dict
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar receita: {str(e)}"
        )

# 🚀 Rota para deletar uma receita por ID
@router.delete("/{receita_id}")
async def deletar_receita(receita_id: str):
    try:
        result = await db.receitas.delete_one({"_id": ObjectId(receita_id)})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receita não encontrada"
            )
        return {"message": "Receita deletada com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar receita: {str(e)}"
        )
