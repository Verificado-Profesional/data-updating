from datetime import datetime
from app.classes.twitter_trends import TwitterTrends
from app.repositories.tendencies_repository import TendenciesRepository
from app.config.config import get_settings
import pandas as pd

settings = get_settings()
# Repository
tendencies_repository = TendenciesRepository(settings.db_name, settings.client)


def update_argentina_twitter_trends():
    twitter_trends = TwitterTrends()
    trends = twitter_trends.get_argentina_trends()

    tendencies_repository.add_twitter_tendencies(trends)
    tendencies_repository.delete_old_twitter_tendencies()
