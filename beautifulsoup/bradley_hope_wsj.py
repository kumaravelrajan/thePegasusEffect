import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd


URLS = ["https://www.theleaflet.in/author/nihalsinghrathod/", "https://www.theleaflet.in/author/nihalsinghrathod/page/2/"]

def parse_article(url):
    print('parsing url', url)
    res = requests.get(url)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text)
    time = soup.find('time', class_='entry-date')
    date_text = soup.find('div', class_='jeg_meta_date').find('a').text
    time = dt.strptime(date_text, '%B %d, %Y')
    title = soup.find('h1').text
    author = soup.find('div', class_='jeg_meta_author').find('a').text
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
        posts_containers = soup.find('div', class_='jnews_author_content_wrapper').find_all('div', class_='jeg_postblock_content')
        for post in posts_containers:
            link = post.find('a').get('href')
            post_data.append(parse_article(link))
            print(post_data[-1])
            # title = post.contents[0].string
            # url = post.contents[0].get('href')
            # time = post.parent.find_next_sibling('article').find(class_='entry-date').find('time').get('datetime')
            # time = datetime.fromisoformat(time)
            #
            # post_data.append({
            #     'title': title,
            #     'url': url,
            #     'time': time,
            # })


    return post_data
