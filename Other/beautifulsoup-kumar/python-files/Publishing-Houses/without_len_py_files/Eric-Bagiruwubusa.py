from bs4 import BeautifulSoup
import requests
import os
import json
import dateutil.parser as parser

from requests.api import head

# Clear terminal before each run
os.system('cls||clear') # this line clears the screen 'cls' = windows 'clear' = unix

journo_name = "Eric-Bagiruwubusa"

listForJson = []

html_text = requests.get(f"https://www.radiyoyacuvoa.com/author/eric-bagiruwubusa/%24qjpp")
soup = BeautifulSoup(html_text.text, 'lxml')

dateList = []
titleList = []
urlList = []

parentElementList = soup.findAll('div', class_="media-block__content media-block__content--h media-block__content--h-xs")

# Collect all dates, titles and urls
for parentElement in parentElementList:
    dateList.append(parser.parse(parentElement.find('span', class_='date date--mb date--size-3').text).isoformat())
    
    stringgg = parentElement.find('h4', class_='media-block__title media-block__title--size-3').text.strip('\n')
    titleList.append(stringgg)

    urlList.append(f"url = https://www.radiyoyacuvoa.com{parentElement.a['href']}")
    
    print("\n\n\n\n")

# create dict for json
for index, date in enumerate(dateList):
    listForJson.append({"title": titleList[index], "time": date, "author": journo_name, "url": urlList[index]}) 

with open(f"/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/beautifulsoup-kumar/json-files/{journo_name}.json", "w") as f:
    f.write(json.dumps(listForJson, indent=4, ensure_ascii=False))
    f.flush()