import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd


URLS = ["https://www.elconfidencial.com/autores/ignacio-cembrero-1484/", "https://www.elconfidencial.com/autores/ignacio-cembrero-1484/2/", "https://www.elconfidencial.com/autores/ignacio-cembrero-1484/3/"]

def parse_article(url):
    print('parsing url', url)
    res = requests.get(url)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text)
    date_text = soup.find('span', class_='dateTime__created').text.strip()
    time = dt.strptime(date_text, '%d/%m/%Y - %H:%M')
    title = soup.find('h1').text.strip()
    author = soup.find('a', class_='authorSignature__link').text.strip()
    return {
        'title': title,
        'url': url,
        'time': time,
        'author': author,
    }


def parse_all():
    post_data = []
    for URL in URLS:
        try:
            res = requests.get(URL)
            assert res.status_code == 200
            soup = BeautifulSoup(res.text)
            article_top_url = soup.find('article', class_='archive-article-top').find('a').get('href')
            post_data.append(parse_article(article_top_url))
            other_articles = soup.find('div', class_='archive-body').find_all('article')
            for post in other_articles:
                link = post.find('a').get('href')
                try:
                    post_data.append(parse_article(link))
                except:
                    print("parsing article failed", link)
                print(post_data[-1])
        except requests.exceptions.TooManyRedirects:
            print("Parsing failed with too many redirects: ", URL)


    return post_data
