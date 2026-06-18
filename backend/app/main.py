from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router as usuarios_router

ORIGENS_FRONTEND = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://172.17.16.1:3001",
]

app = FastAPI(title="Wizardry API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGENS_FRONTEND,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(usuarios_router)


@app.get("/health")
def verificar_saude() -> dict[str, str]:
    return {"status": "ok"}
