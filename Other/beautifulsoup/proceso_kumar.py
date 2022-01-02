from bs4 import BeautifulSoup
import requests
import os
import json
import dateutil.parser as parser
import cloudscraper

from requests.api import head

# Clear terminal before each run
# os.system('cls||clear') # this line clears the screen 'cls' = windows 'clear' = unix

journo_name = "Rafale-Rodriguez-Castaneda"

listForJson = []
dateList = []
titleList = []
urlList = []

scraper = cloudscraper.create_scraper()
html_text = scraper.get("https://www.proceso.com.mx/autor/rafael-rodriguez-castaneda.html").text
soup = BeautifulSoup(html_text, 'lxml')

parentElementsList =  soup.findAll('article', class_='article-bandera')

for parentElement in parentElementsList:
    titleList.append(parentElement.find('h5', class_="titulo").a.text)
    urlList.append('https://www.proceso.com.mx' + parentElement.find('h5', class_="titulo").a['href'])
    dateList.append(parser.parse(parentElement.find('span', class_='hora').text[:-3]).isoformat())

# create dict for json
for index, date in enumerate(dateList):
    listForJson.append({"title": titleList[index], "time": date, "author": journo_name, "url": urlList[index]})

with open(f"{journo_name}.json", "w") as f:
    f.write(json.dumps(listForJson, indent=4, ensure_ascii=False))
    f.flush()