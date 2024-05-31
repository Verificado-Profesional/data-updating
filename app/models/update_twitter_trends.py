from app.classes.twitter_trends import TwitterTrends
from app.config.constants import ARGENTINA_TWITTER_URL, BSAS_TWITTER_URL, CORDOBA_TWITTER_URL, ROSARIO_TWITTER_URL
from app.repositories.tendencies_repository import TendenciesRepository
from app.config.config import get_settings

settings = get_settings()
# Repository
tendencies_repository = TendenciesRepository(settings.db_name, settings.client)

def update_trends(trends):
    trends_grouped = trends.groupby(['date', 'tweet', 'url', 'region']).agg({'tweet_count': 'sum'}).reset_index()

    trends_grouped = trends_grouped.nlargest(15, 'tweet_count').reset_index(drop=True)

    region_names = {ARGENTINA_TWITTER_URL: ARGENTINA_TWITTER_URL, ROSARIO_TWITTER_URL: "rosario", CORDOBA_TWITTER_URL: "cordoba", BSAS_TWITTER_URL: "buenos-aires"}
    trends_grouped['region'] = trends_grouped['region'].apply(lambda x: region_names[x])

    tendencies_repository.add_twitter_tendencies(trends_grouped)
    tendencies_repository.delete_old_twitter_tendencies()

def update_argentina_twitter_trends():
    twitter_trends = TwitterTrends()
    argentina_trends = twitter_trends.get_region_trends(ARGENTINA_TWITTER_URL)
    buenos_aires_trends = twitter_trends.get_region_trends(BSAS_TWITTER_URL)
    rosario_trends = twitter_trends.get_region_trends(ROSARIO_TWITTER_URL)
    cordoba_trends = twitter_trends.get_region_trends(CORDOBA_TWITTER_URL)

    update_trends(argentina_trends)
    update_trends(buenos_aires_trends)
    update_trends(rosario_trends)
    update_trends(cordoba_trends)
    
