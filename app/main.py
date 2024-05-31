import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.config import get_settings
from app.repositories.tendencies_repository import TendenciesRepository

from .routers import update_trends

origins = ["*"]
app = FastAPI()
app.include_router(update_trends.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


def start():
    settings = get_settings()
    TendenciesRepository(settings.db_name, settings.client)
    print("connected database!")
    """Launched with `poetry run start` at root level"""
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)


@app.get("/")
def root():
    return {"message": "Hola, Verificados!"}
