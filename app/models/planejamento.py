from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import date

class Planejamento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    data: date  # Campo de data
    receita_id: int = Field(foreign_key="receita.id")
    refeicao: str

    receita: Optional["Receita"] = Relationship(back_populates="planejamentos")

class PlanejamentoCreate(SQLModel):
    data: str  # Entrada como string
    receita_id: int
    refeicao: str

