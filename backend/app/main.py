from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.produto_router import router as produtos_router
from app.api.router import router as usuarios_router

ORIGEM_FRONTEND = "http://localhost:3000"

app = FastAPI(title="Magic Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ORIGEM_FRONTEND],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_router)
app.include_router(produtos_router)


@app.get("/health")
def verificar_saude() -> dict[str, str]:
    return {"status": "ok"}
