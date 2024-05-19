from datetime import datetime
from app.repositories.tendencies_repository import TendenciesRepository
from app.classes.google_trends import GoogleTrends
from app.config.config import get_settings
import pandas as pd

settings = get_settings()
# Repository
tendencies_repository = TendenciesRepository(settings.db_name, settings.client)


def update_argentina_google_trends(date=datetime.today()):
    google_trends = GoogleTrends('es-AR')
    trends = google_trends.get_trends("argentina")
    trends['date'] = date.strftime('%d-%m-%Y')
    trends.rename(columns={0: "trend"}, inplace=True)
    
    keywords= trends.trend.tolist()

    province_trends = google_trends.trends_by_country(keywords)
    province_trends = province_trends.transpose()
    province_trends.columns = province_trends.iloc[0]
    province_trends = province_trends.drop(province_trends.index[0])
    merged_df = pd.merge(province_trends, trends, left_index=True, right_on='trend')

    tendencies_repository.add_google_tendencies(merged_df)
    tendencies_repository.delete_old_twitter_tendencies()
