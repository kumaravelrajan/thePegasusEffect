import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import locale
from datetime import datetime
import cloudscraper

URLS = ["https://www.eluniversal.com.mx/autor-opinion/columnistas/ricardo-raphael/politica-zoom"]
BASE_URL = 'https://www.eluniversal.com.mx'

scraper = cloudscraper.CloudScraper()

def parse_article(url):
    print('parsing url', url)
    res = scraper.get(url)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text)
    views = soup.find_all('div', class_='view-content')
    title = views[0].find('h1').text.strip()
    author = views[0].find('a').text.strip()
    date_text = views[1].find('a', class_='ce12-DatosArticulo_ElementoFecha').text.strip()
    time = dt.strptime(date_text, '%d/%m/%Y')
    main_text = soup.find('div', class_='field-type-text-with-summary').text.strip()
    length = len(main_text.replace('\n', ' ').split(' '))
    return {
        'title': title,
        'url': url,
        'time': time,
        'author': author,
        'length': length,
    }


def parse_all():
    # for date parsing in spanish
    # note that the es_ES.UTF-8 locale must be installed on your computer!
    locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

    post_data = []
    for URL in URLS:
        res = scraper.get(URL)
        assert res.status_code == 200
        soup = BeautifulSoup(res.text)
        articles = soup.find_all('div', class_='view-content')[2].find_all('div', class_='views-row')
        for article in articles:
            url = article.find('a').get('href')
            post_data.append(parse_article(BASE_URL + url))

    return post_data
