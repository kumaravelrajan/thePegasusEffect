import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import locale
from datetime import datetime


URLS = ["https://quintoelab.org/noticias"]
# BASE_URL = 'https://www.humanite.fr'

def parse_time(url):
    print('parsing url', url)
    res = requests.get(url)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text)
    possible_date_texts = map(lambda x: x.text.strip(), soup.find_all('span', style='color: rgb(73, 73, 73);'))
    time = None
    for date_text in possible_date_texts:
        try:
            time = dt.strptime(date_text, '%d de %B de %Y')
        except:
            try:
                time = time = dt.strptime(date_text, '%d de %B %Y')
            except:
                continue
        break
    if not time:
        possible_date_texts_2 = map(lambda x: x.text.strip(),
                                    soup.find_all('span', style='color: rgb(255, 255, 255);'))
        for date_text in possible_date_texts_2:
            try:
                time = dt.strptime(date_text, '%d %B %Y')
            except:
                try:
                    time = dt.strptime(date_text, '%d de %B de %Y')
                except:
                    continue
                break
            break
    if not time:
        raise Exception('could not parse time')
    return time


def parse_all():
    # for date parsing in french
    # note that the es_ES.UTF-8 locale must be installed on your computer!
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

    post_data = []
    for URL in URLS:
        res = requests.get(URL)
        assert res.status_code == 200
        soup = BeautifulSoup(res.text)
        articles = soup.find_all('div', class_='home-post')
        for article in articles:
            title = article.find('div', class_='home-title').text
            url = article.find('a', class_='block-link').get('href')
            author = article.find('div', class_='home-author').find('span').text
            time = parse_time(url)
            post_data.append({
                'title': title,
                'url': url,
                'time': time,
                'author': author,
            })

    return post_data
