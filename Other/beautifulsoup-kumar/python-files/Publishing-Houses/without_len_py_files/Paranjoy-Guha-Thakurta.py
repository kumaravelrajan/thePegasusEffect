from bs4 import BeautifulSoup
import requests
import os
import json
import dateutil.parser as parser

from requests.api import head

# Clear terminal before each run
os.system('cls||clear') # this line clears the screen 'cls' = windows 'clear' = unix

journo_name = "paranjoy_guha_thakurta"

listForJson = []
dateList = []
titleList = []
urlList = []

# all articles
pageCounter = 0
isEnd = False
while True:
    html_text = requests.get(f"https://paranjoy.in/articles?page={pageCounter}")
    soup = BeautifulSoup(html_text.text, 'lxml')

    ParentElementsList = soup.findAll('div', class_='node node-article view-mode-article_teaser clearfix')

    for ParentElement in ParentElementsList:
        if((parser.parse(ParentElement.find('span', class_="date-display-single").text) - parser.parse("2018-12-31T00:00:00")).days > 0):
            dateList.append(parser.parse(ParentElement.find('span', class_="date-display-single").text).isoformat())
            titleList.append(ParentElement.find('h5', class_=['head', 'head-h', 'head-b']).a.text)
            urlList.append("https://paranjoy.in" + ParentElement.find('h5', class_=['head', 'head-h', 'head-b']).a['href'])
        else:
            isEnd = True
            break

    if(isEnd):
        break
    else:
        # increment counter
        pageCounter += 1

# all videos
pageCounter = 0
isEnd = False
while True:
    html_text2 = requests.get(f"https://paranjoy.in/videos?page={pageCounter}")
    soup2 = BeautifulSoup(html_text2.text, 'lxml')

    ParentElementsList2 = soup2.findAll('div', class_='node node-video view-mode-video_excerpt clearfix')

    for ParentElement2 in ParentElementsList2:
        if((parser.parse(ParentElement2.find('span', class_="date-display-single").text) - parser.parse("2018-12-31T00:00:00")).days > 0):
            dateList.append(parser.parse(ParentElement2.find('span', class_="date-display-single").text).isoformat())
            titleList.append(ParentElement2.find('h6', 'head video-space').a.text)
            urlList.append("https://paranjoy.in" + ParentElement2.find('h6', 'head video-space').a['href'])
        else:
            isEnd = True
            break

    if(isEnd):
        break
    else:
        # increment counter
        pageCounter += 1

# create dict for json
for index, date in enumerate(dateList):
    listForJson.append({"title": titleList[index], "time": date, "author": journo_name, "url": urlList[index]}) 

with open(rf"C:\Users\kumar\Desktop\TUM\Seminar\pegasus_cybercrime_seminar_latest\Other\beautifulsoup-kumar\json-files\{journo_name}_withoutLen.json", "w", encoding='utf8') as f:
    f.write(json.dumps(listForJson, indent=4, ensure_ascii=False))
    f.flush()