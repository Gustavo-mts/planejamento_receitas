from typing import List, Optional
from sqlmodel import SQLModel, Field
from app.models.ingrediente import Ingrediente
from app.models.planejamento import Planejamento

class ReceitaResponse(SQLModel):
    id: int
    nome: str
    tempo_preparo: int
    descricao: Optional[str]
    porcoes: int
    nivel_dificuldade: str
    calorias: int
    instrucoes: str
    ingredientes: List[Ingrediente] = []
    planejamentos: List[Planejamento] = []
