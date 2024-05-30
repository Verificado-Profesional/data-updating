import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
from datetime import timedelta

class TwitterTrends():
  def get_trends(region):
    url = f'https://trends24.in/{region}/'
    response = requests.get(url)

    if response.status_code != 200:
        print('Error al obtener la página:', response.status_code)
        return

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    trends = soup.find_all('div', class_='trend-card')
    tendencias = defaultdict(list)

    for trend_card in trends:
        fecha = trend_card.find('h5', class_='trend-card__time').text
        tendencias_list = trend_card.find_all('li')
        for tendencia in tendencias_list:
            tweet_count = tendencia.find('span', class_='tweet-count')
            if not tweet_count:
               continue

            tweet_count = tweet_count.text.strip()
            tweet_count = int(tweet_count[:-1]) * 1000
            nombre_tendencia = tendencia.a.text.strip()
            url_tendencia = tendencia.a['href']
            tendencias[fecha].append({
                        'date': fecha,
                        'tweet': nombre_tendencia,
                        'url': url_tendencia,
                        'tweet_count': tweet_count,
                        'region': region
                    })


    df = pd.concat([pd.DataFrame(data) for data in tendencias.values()], ignore_index=True)
    tendencias = dict(sorted(tendencias.items(),reverse=True))

    return tendencias,df
  
  def get_region_trends(self, region):
    tendencias,df = TwitterTrends.get_trends(region)

    df["datetime"]= pd.to_datetime(df["date"],dayfirst=True)
    df['datetime_arg'] = df['datetime'] - timedelta(hours=3)    
    df['datetime_arg'] = df['datetime_arg'].dt.day
    
    return df


    

