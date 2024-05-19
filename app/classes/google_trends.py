import pandas as pd
import matplotlib.pyplot as plt
from pytrends.request import TrendReq
from matplotlib.dates import DateFormatter
from datetime import datetime, timedelta

class GoogleTrends():

  def __init__(self,region):
    self.region = region
    self.pytrends = TrendReq(hl=region, tz=360)

  def get_trends(self,region):
    trends = self.pytrends.trending_searches(pn=region)
    return trends

  def trends_by_time(self, keywords,timeframe='now 1-d' ):
    df_trends = pd.DataFrame()
    first = True

    for trend in keywords:
      self.pytrends.build_payload(kw_list=[trend], timeframe=timeframe, geo='AR')
      df_google_trends= self.pytrends.interest_over_time()
      df_google_trends.reset_index(inplace=True)
      df_google_trends = df_google_trends.loc[:,["date",trend]]
      if first:
        df_trends = df_google_trends
        first=False
      else:
        df_trends  = pd.merge(df_trends, df_google_trends,on='date', how='outer')

    return df_trends

  def trends_by_country(self, keywords,timeframe='now 1-d' ):

    trends_by_provincia = pd.DataFrame()
    first = True
    for trend in keywords:
      self.pytrends.build_payload(kw_list=[trend], timeframe=timeframe, geo='AR')
      df_google_trends= self.pytrends.interest_by_region(resolution="COUNTRY")
      df_google_trends.reset_index(inplace=True)
      df_google_trends = df_google_trends.loc[:,["geoName",trend]]

      if first:
        trends_by_provincia = df_google_trends
        first=False
      else:
        trends_by_provincia  = pd.merge(trends_by_provincia, df_google_trends,on='geoName', how='outer')

    return trends_by_provincia
  
  

