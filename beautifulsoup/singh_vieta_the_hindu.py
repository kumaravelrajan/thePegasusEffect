import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd


URLS = [f"https://www.thehindu.com/profile/author/?page={i}&urlSuffix=Vijaita-Singh-684" for i in range(111, 150)]

def parse_article(url):
    print('parsing url', url)
    res = requests.get(url)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text)
    try:
        author = soup.find('a', class_='auth-nm').text.strip()
    except:
        author = ''
    date_text = soup.find('div', class_='author-container').find('none').text.strip()
    try:
        title = soup.find('h1', class_='title').text.strip()
    except AttributeError:
        try:
            title = soup.find('h2', class_='special-article-heading').text.strip()
        except AttributeError:
            title = ''
    time = dt.strptime(date_text[:-4], '%B %d, %Y %H:%M')

    return {
        'title': title,
        'url': url,
        'time': time,
        'author': author,
    }


def parse_all():
    post_data = []
    for URL in URLS:
        res = requests.get(URL)
        assert res.status_code == 200
        soup = BeautifulSoup(res.text)
        top_part = soup.find_all('div', class_='story-card-33')
        for article in top_part:
            url = article.find('p', class_='story-card-33-heading').find('a').get('href')
            post_data.append(parse_article(url))
        bottom_part = soup.find_all('div', 'story-card-news')
        for article in bottom_part:
            url = article.find('h3').find('a').get('href')
            post_data.append(parse_article(url))

    return post_data
