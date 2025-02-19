from sqlmodel import SQLModel, Field

class ReceitaIngrediente(SQLModel, table=True):
    receita_id: int = Field(foreign_key="receita.id", primary_key=True)
    ingrediente_id: int = Field(foreign_key="ingrediente.id", primary_key=True)
