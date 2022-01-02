import locale

import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import json
import cloudscraper

AUTHOR_NAME = 'Alvaro Delgado'
HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5'}

URL = 'https://www.proceso.com.mx/a/aps/noticias/paginas/ajax/autor.asp'
BASE_URL = 'https://www.proceso.com.mx'
data = {
    'id_autor': 2,
    'page': 1,
}


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, dt):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


scraper = cloudscraper.CloudScraper()

def parse_article(url):
    print('parsing url', url)
    res = scraper.get(url, headers=HEADERS)
    assert res.status_code == 200
    soup = BeautifulSoup(res.content.decode('utf-8'))
    title = soup.find('h1').text.strip()
    author = soup.find('span', class_='post-author-name').text.strip()
    date_text = soup.find('div', class_='fecha').text.strip()
    time = dt.strptime(date_text, '%A, %d de %B de %Y')
    length = len(soup.find('div', class_='cuerpo-nota').text.strip().replace('\n', ' ').strip(' '))
    return {
        'title': title,
        'url': url,
        'time': time,
        'author': author,
        'length': length,
    }


def parse_all():
    post_data = []

    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

    i = 1
    while True:

        data['page'] = i
        res = scraper.post(URL, data=data)
        assert res.status_code == 200
        if len(res.text) == 0:
            break
        soup = BeautifulSoup(res.text)
        articles = soup.find_all('article', class_='article-bandera')
        for article in articles:
            link = BASE_URL + article.find('a').get('href')
            post_data.append(parse_article(link))
            print(len(post_data), post_data[-1])
        i += 1


    return post_data


post_data = parse_all()

journalist_name = 'Alvaro Delgado'

with open(f"{journalist_name.replace(' ', '_').lower()}.json", 'w') as f:
    json.dump(post_data, f, default=json_serial)
