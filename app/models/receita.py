from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class Receita(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")  # O _id do MongoDB será convertido para string
    nome: str
    tempo_preparo: int
    descricao: Optional[str] = None
    porcoes: int
    nivel_dificuldade: str
    calorias: int
    instrucoes: str

    # Ingredientes serão armazenados como lista de ObjectId
    ingredientes: Optional[List[str]] = []  # Lista de IDs dos ingredientes

    # Planejamentos também serão referenciados por IDs
    planejamentos: Optional[List[str]] = []

    class Config:
        orm_mode = True  # Permite compatibilidade com ORM, se necessário
        json_encoders = {ObjectId: str}  # Converte ObjectId para string automaticamente

