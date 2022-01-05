import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import locale
from datetime import datetime


# URLS = ['https://www.independantexpress.net/author/ericg/']
URLS = [f'https://www.independantexpress.net/author/ericg/page/{i}/' for i in range(1, 21)]
# URLS = [f'https://www.independantexpress.net/author/ericg/page/{i}/' for i in range(13, 14)]

HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5'}

TRANSLATE = { 'janv': 'janv.', 'févr': 'févr.', 'avr': 'avr.', 'juil': 'juil.', 'sep': 'sept.', 'oct': 'oct.', 'nov': 'nov.', 'déc': 'déc.'}


def trans_strings(s, translation):
    for k, v in translation.items():
        s = s.replace(k, v)
    return s

def parse_article(url):
    print('parsing url', url)
    res = requests.get(url, headers=HEADERS)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text)
    if not soup.find('u', text='Carlos KETOHOU'):
        return None
    body = soup.find('div', class_='continue-reading-content')
    length = len(list(filter(lambda x: len(x.strip()) != 0, body.text.replace('\n', ' ').split(' '))))
    title = soup.find('span', class_='post-title').text
    date_text = soup.find('div', class_='post-meta-wrap').find('time').find('b').text
    time = datetime.strptime(trans_strings(date_text.lower(), TRANSLATE), '%b %d, %Y')
    author = 'Carlos Ketohou'


    return {
        'title': title,
        'url': url,
        'time': time,
        'author': author,
    }


def parse_all():
    # for date parsing in french
    # note that the fr_FR.UTF-8 locale must be installed on your computer!
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

    post_data = []

    for URL in URLS:
        # the website blocks us with a 406 if we don't provide a Mozilla User Agent
        res = requests.get(URL, headers=HEADERS)
        assert res.status_code == 200
        soup = BeautifulSoup(res.text)
        articles = soup.find_all('article', class_='type-post')
        for article in articles:
            url = article.find('h2').find('a').get('href')
            post = parse_article(url)
            if post:
                post_data.append(post)

    return post_data
