from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from app.models.receita_ingrediente import ReceitaIngrediente

class Ingrediente(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    quantidade: float
    unidade_medida: str

    receitas: List["Receita"] = Relationship(
        back_populates="ingredientes",
        link_model=ReceitaIngrediente  # Tabela intermediária
    )