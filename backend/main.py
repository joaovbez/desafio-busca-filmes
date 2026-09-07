from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.search import router

app = FastAPI(title="Busca de Filmes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(router)
