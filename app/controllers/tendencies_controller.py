from fastapi import Request, HTTPException, status
from app.config.config import get_settings
from app.models.update_google_trends import update_argentina_google_trends
from app.models.update_twitter_trends import update_argentina_twitter_trends
from app.repositories.tendencies_repository import TendenciesRepository

settings = get_settings()
# Repository
tendencies_repository = TendenciesRepository(settings.db_name, settings.client)


class TendenciesController:

    @staticmethod
    def update_trends():
        try:
            TendenciesRepository(settings.db_name, settings.client)
            print("connected database!")
            """Launched with `poetry run start` at root level"""
            update_argentina_twitter_trends()
            update_argentina_google_trends()
        except Exception:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Could not update trends"
        )
        
        