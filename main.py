# -*- coding: utf-8 -*-
import requests
import os

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API = os.environ.get('STOCK_API')
NEWS_API = os.environ.get('NEWS_API')

# Getting information about stock changes between yesterday and the day before yesterday.
params_stock = {'function': 'TIME_SERIES_DAILY',
                'symbol': STOCK,
                'apikey': STOCK_API}

response = requests.get(url=STOCK_ENDPOINT, params=params_stock)
response.raise_for_status()
stock_data = response.json()

yesterday = list(stock_data['Time Series (Daily)'].keys())[0]
day_before = list(stock_data['Time Series (Daily)'].keys())[1]

close_yesterday = float(stock_data['Time Series (Daily)'][yesterday]['4. close'])
close_day_before = float(stock_data['Time Series (Daily)'][day_before]['4. close'])

# Getting 3 news articles about the indicated company if the stock difference is greater than 2% and saving them to a
# separate file.
if abs(close_day_before - close_yesterday) >= close_yesterday * 0.02:
    percent = round(((close_yesterday - close_day_before) / close_yesterday) * 100, 2)
    params_news = {'q': COMPANY_NAME,
                   'apiKey': NEWS_API}

    response_news = requests.get(url=NEWS_ENDPOINT, params=params_news)
    response_news.raise_for_status()
    news_data = response_news.json()
    three_news = news_data['articles'][0:3]

    with open('news_file.txt', 'w') as f:
        f.write(f"{COMPANY_NAME}: {percent}%\n")
        for item in three_news:
            f.write(f"Headline: {item['description']}\n")
