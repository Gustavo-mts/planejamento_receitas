from fastapi import FastAPI
from app.routes.receitas import router as receita_router  # Certifique-se de importar o roteador corretamente

app = FastAPI(title="API de Receitas com MongoDB")

# Registrar as rotas corretamente
app.include_router(receita_router)

@app.get("/")
async def root():
    return {"message": "API FastAPI + MongoDB funcionando!"}
