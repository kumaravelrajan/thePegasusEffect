from datetime import date
from bs4 import BeautifulSoup
import requests
import os
import json
import dateutil.parser as parser

from requests.api import head

# Clear terminal before each run
os.system('cls||clear') # this line clears the screen 'cls' = windows 'clear' = unix

journo_name = "Carmen-Aristegui"

listForJson = []
dateList = []
titleList = []
urlList = []

# Parse all default 20 articles
session = requests.session()
html_text = session.get(f"https://cnnespanol.cnn.com/author/carmen-aristegui/")
soup = BeautifulSoup(html_text.text, 'lxml')

allArticles = soup.findAll('h2', class_=['news__title'])

for article in allArticles:
    titleList.append(article.a['title'])
    urlList.append(article.a['href'])

    # Fetch each individual article's page to get date.
    html_text = session.get(article.a['href'])
    soup = BeautifulSoup(html_text.text, 'lxml')
    dateList.append(parser.parse(soup.find('time', class_='news__date')['datetime']).isoformat())

# Parse all further loaded articles.
count = 20
isEnd = False

spanishToEnglishMonths = {
    'enero' : 'january', 
    'febrero' : 'february', 
    'marzo' : 'march', 
    'abril' : 'april', 
    'mayo' : 'may', 
    'junio' : 'june', 
    'julio' : 'july', 
    'agosto' : 'august', 
    'septiembre' : 'september', 
    'octubre' :'october', 
    'noviembre' :'november', 
    'diciembre' : 'december'
}

while True:
    html_text = requests.get(f'https://cnnespanol.cnn.com/ajax/load-posts/author/carmen-aristegui/0/{count}/default-tag')

    soup = BeautifulSoup(html_text.text, 'lxml')
    allArticles = soup.findAll('h2', class_=['news__title'])

    for article in allArticles:
        html_text = session.get(article.a['href'])
        soup = BeautifulSoup(html_text.text, 'lxml')

        try:
            pubDate = parser.parse(soup.find('time', class_=['news__date'])['datetime'])
        except:
            pubDateSpanishToEnglish = soup.find('time', class_=['storyfull__time']).text.split()
            pubDateSpanishToEnglish[4] = spanishToEnglishMonths[pubDateSpanishToEnglish[4][:-1]]
            pubDate = parser.parse(' '.join(pubDateSpanishToEnglish[3:]))

        if((pubDate - parser.parse("2016-12-31")).days > 0):
            dateList.append(pubDate.isoformat())
            titleList.append(article.a['title'])
            urlList.append(article.a['href'])
        else:
            isEnd = True
            break

    if(isEnd):
        break
    else:
        count += 9

# create dict for json
for index, date in enumerate(dateList):
    listForJson.append({"title": titleList[index], "time": date, "author": journo_name, "url": urlList[index]}) 

with open(rf"C:\Users\kumar\Desktop\TUM\Seminar\pegasus_cybercrime_seminar_latest\Other\beautifulsoup-kumar\json-files\Publishing-Houses\{journo_name}Copy.json", "w", encoding='utf8') as f:
    f.write(json.dumps(listForJson, indent=4, ensure_ascii=False))
    f.flush()