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
    trends['date'] = pd.to_datetime(trends['date'], format='%d-%m-%Y %H:%M:%S')
    trends['date'] = trends['date'].dt.strftime('%d-%m-%Y')
    trends_grouped = trends.groupby(['date', 'tweet', 'url']).agg({'tweet_count': 'sum'}).reset_index()

    tendencies_repository.add_twitter_tendencies(trends_grouped)
    tendencies_repository.delete_old_twitter_tendencies()
