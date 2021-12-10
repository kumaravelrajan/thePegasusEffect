import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd


URLS = [f"https://thewire.in/author/svaradarajan"]

BASE_URL = 'https://thewire.in'

JSON_URL = 'https://thewire.in/wp-json/thewire/v2/posts/author/%s/?per_page=%d&page=%d&type=opinion'

def json(author):
    per_page = 100
    post_data = []
    author_map = {}
    i = 0
    while True:
        res = requests.get(JSON_URL % (author, per_page, i))
        i+=1
        if res.status_code != 200:
            break
        resp_json = res.json()
        author_list = resp_json['author-profile']
        for a in author_list:
            if a['author_id'] not in author_map:
                author_map[a['author_id']] = a['author_display_name']
        articles = resp_json['author-archives']
        if len(articles) == 0:
            break
        for article in articles:
            post_data.append({
                'title': article['post_title'],
                'url': article['guid'],
                'time': article['post_date'],
                'author': author_map[int(article['post_author'])],
            })
        print('Total scraped posts', len(post_data))
    return post_data

def parse_article(url):
    print('parsing url', url)
    res = requests.get(url)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text)
    author = soup.find('div', class_='author__name').find('a').text.strip()
    title = soup.find('h1', class_='title').text.strip()
    date_text = soup.find('span', class_='posted-on').text.strip()
    time = dt.strptime(date_text, '%d/%b/%Y')

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
        cards = soup.find('div', id='authorAllPostsContainer').find_all('div', class_='card')
        for card in cards:
            relative_url = card.find('a').get('href')
            post_data.append(parse_article(BASE_URL + relative_url))

    return post_data
