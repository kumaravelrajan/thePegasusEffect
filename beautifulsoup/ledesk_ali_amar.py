import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import locale
from datetime import datetime


PAGE_URL = 'https://ledesk.ma/author/aliamar/'
AJAX_URL = 'https://ledesk.ma/ajax/'

# Le Desk's website seems to be broken: Only the initial 12 articles that are loaded on the author's
# page actually belong to the respective authors. All articles loaded by the AJAX functionality
# belong to any author of the publishing house

# URLS = [f"https://www.humanite.fr/auteurs/rosa-moussaoui?page={i}" for i in range(0, 55)]
# BASE_URL = 'https://www.humanite.fr'

def parse_article(url):
    print('parsing url', url)
    res = requests.get(url)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text)
    body = soup.find('div', class_='group-ft-header-node-article')
    title = body.find('div', class_='field-name-title').find('h1').text
    date_text = body.find('div', class_='group-ft-auteur-date-media').find('span', class_='date-display-single').text
    time = datetime.strptime(date_text, "%A %d %B %Y")
    author = body.find('div', class_='group-ft-auteur-date-media').find('div', class_='field-name-field-news-auteur').find('a').text


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

    # for ajax we need session cookies
    sess = requests.Session()
    res = sess.get(PAGE_URL)
    assert res.status_code == 200

    res = sess.post(AJAX_URL, data={
        'container': '.box-push-author',
        'aid': 2,
        'posts_per_page': 12,
        'offset': 12,
        'type': 'author',
        'action': 'load_more'
    }, headers={'referer': 'https://ledesk.ma/author/aliamar/'})
    assert res.status_code == 200
    soup = BeautifulSoup(res.text)
    posts = soup.find_all('div', class_='box-push')
    for post in posts:
        url = post.find('a').get('href')
        posts.append(parse_article(url))
    # while res.status_code == 200:


    # for URL in URLS:
    #     res = requests.get(URL)
    #     assert res.status_code == 200
    #     soup = BeautifulSoup(res.text)
    #     articles = soup.find('div', id='content').find('div', class_='view-content').find_all('div', class_='group-description')
    #     for article in articles:
    #         url = article.find('div', class_='field-name-title').find('a').get('href')
    #         post_data.append(parse_article(BASE_URL + url))

    return post_data
