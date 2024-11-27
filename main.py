from fastapi import FastAPI
from core.configs import settings
from api.v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="Trabalho de EMPR")

# Configuração do CORS
origins = [
    "http://localhost",  # Permite o acesso de localhost
    "http://localhost:5500", # Se seu frontend estiver rodando em localhost:3000 (React, Vue, etc.)
    "http://127.0.0.1:5500",  # Caso use o 127.0.0.1 no lugar de localhost
]

# Adiciona o middleware CORS ao FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Define quais domínios podem fazer requisição
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

app.include_router(api_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=True)   


