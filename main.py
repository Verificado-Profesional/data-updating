import uvicorn
from app.config.config import get_settings
from app.models.update_twitter_trends import update_argentina_twitter_trends
from app.repositories.tendencies_repository import TendenciesRepository

origins = ["*"]

def start():
    settings = get_settings()
    TendenciesRepository(settings.db_name, settings.client)
    print("connected database!")
    """Launched with `poetry run start` at root level"""
    update_argentina_twitter_trends()
   # uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)


if __name__ == "__main__":
    start()