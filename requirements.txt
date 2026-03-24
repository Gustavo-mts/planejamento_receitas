# 📌 API de Planejamento de Receitas com FastAPI e MongoDB

API para gerenciamento de receitas utilizando **FastAPI** e **MongoDB**.

## 🚀 Tecnologias Utilizadas

- **FastAPI** → Framework web moderno e rápido ⚡
- **MongoDB** → Banco de dados NoSQL para armazenamento dos dados
- **Motor** → Driver assíncrono para MongoDB
- **Uvicorn** → Servidor ASGI para rodar a aplicação
- **Pydantic** → Modelagem e validação de dados
- **Python-Dotenv** → Gerenciamento de variáveis de ambiente

## ⚙️ Configuração do Ambiente

### 🔹 1. Clonar o Repositório

```bash
git clone https://github.com/Gustavo-mts/planejamento_receitas.git
cd planejamento_receitas
```


### 🔹 2. Criar um Ambiente Virtual (Opcional)

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate      # Windows
```

### 🔹 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 🔹 4. Configurar Variáveis de Ambiente

```
MONGO_URI=mongodb://localhost:27017/api_db
```


## 🔧 Rodando a Aplicação

### 🔹 1. Iniciar o MongoDB
```bash
sudo systemctl start mongod
```

### 🔹 2. Iniciar a API
```
uvicorn app.main:app --reload
```