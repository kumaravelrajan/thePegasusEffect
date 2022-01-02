import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import locale
import json


URL = 'https://caspiandefense.wordpress.com/?infinity=scrolling'

data = {
    'action': 'infinite_scroll',
    'page': 0,
    'order': 'DESC',
}

def parse_article(url):
    res = requests.post(url)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text)
    title = soup.find('article').find('h1').text.strip()
    date_text = soup.find('article').find('div', class_='entry-meta').find('a').text
    time = dt.strptime(date_text, '%d. %B %Y')
    author = 'Caspian Defense'
    length = len(soup.find('div', class_='entry-content').text.strip().replace('\n', ' ').split(' '))
    return {
        'title': title,
        'url': url,
        'time': time,
        'author': author,
        'length': length,
    }
post_data = []
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # for some reason dates are in German :(

i = 0
while True:
    data['page'] = i
    res = requests.post(URL, data=data)
    assert res.status_code == 200
    print(res.text)
    json_data = res.json()
    soup = BeautifulSoup(json_data['html'])

    articles = soup.find_all('article')
    for article in articles:
        url = article.find('a').get('href').strip()
        post_data.append(parse_article(url))
    if json_data['lastbatch']:
        break
    i += 1


journalist_name = 'Jasur Sumerinli'

with open(f"{journalist_name.replace(' ', '_').lower()}.json", 'w') as f:
    json.dump(post_data, f, default=json_serial)
