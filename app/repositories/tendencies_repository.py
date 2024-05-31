from cpunk_mongo.db import DataBase
from pymongo import MongoClient
from datetime import datetime, timedelta

from app.config.constants import GOOGLE, TWITTER


class TendenciesRepository(DataBase):
    def __init__(self, db_name, url):
        if db_name == "test":
            import mongomock  # type: ignore

            self.db = mongomock.MongoClient().db
        else:
            self.client = MongoClient(url)
            self.db = self.client.mongodb_client[db_name]
            self.twitter_collection = self.db[TWITTER]
            self.google_collection = self.db[GOOGLE]

    def add_google_tendencies(self, tendencies_df):
        data_dict = tendencies_df.to_dict(orient='records')
        self.google_collection.insert_many(data_dict)

    def add_twitter_tendencies(self, tendencies_df):
        data_dict = tendencies_df.to_dict(orient='records')
        self.twitter_collection.insert_many(data_dict)

    def delete_old_twitter_tendencies(self):
        one_month_ago = datetime.now() - timedelta(days=30)
        query = {'fecha': {'$lt': one_month_ago}}
        self.twitter_collection.delete_many(query)
