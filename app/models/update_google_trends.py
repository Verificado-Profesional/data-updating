from datetime import datetime, timedelta
from app.repositories.tendencies_repository import TendenciesRepository
from app.classes.google_trends import GoogleTrends
from app.config.config import get_settings
import pandas as pd

settings = get_settings()
# Repository
tendencies_repository = TendenciesRepository(settings.db_name, settings.client)

def get_suma_tendencias(df, keywords):
        suma_total = df[keywords].sum()
        suma_tendencias = {}

        for tendencia, suma in suma_total.items():
            suma_tendencias[tendencia] = suma
            
        return suma_tendencias


def update_argentina_google_trends(date=datetime.today()):
    google_trends = GoogleTrends('es-AR')
    trends = google_trends.get_trends("argentina")
    trends['date'] = date.strftime('%d-%m-%Y')
    trends.rename(columns={0: "trend"}, inplace=True)
    
    keywords= trends.trend.tolist()

    province_trends = google_trends.trends_by_country(keywords)
    province_trends['geoName'] = province_trends['geoName'].apply(lambda x: "_".join(x.lower().split(" ")))
    province_trends = province_trends.transpose()
    province_trends.columns = province_trends.iloc[0]
    province_trends = province_trends.drop(province_trends.index[0])
    merged_df = pd.merge(province_trends, trends, left_index=True, right_on='trend')

    trends_by_time = google_trends.trends_by_time(keywords)
    trends_by_time = trends_by_time.fillna(0)
    trends_by_time['datetime'] = pd.to_datetime(trends_by_time['date'])
    trends_by_time['datetime_arg'] = trends_by_time['datetime'] - timedelta(hours=3)

    suma_tendencias = get_suma_tendencias(trends_by_time,keywords)
    merged_df['cantidad_busquedas'] = merged_df['trend'].apply(lambda x: suma_tendencias[x])

    print("merged df: \n", merged_df)

    tendencies_repository.add_google_tendencies(merged_df)
    tendencies_repository.delete_old_twitter_tendencies()
