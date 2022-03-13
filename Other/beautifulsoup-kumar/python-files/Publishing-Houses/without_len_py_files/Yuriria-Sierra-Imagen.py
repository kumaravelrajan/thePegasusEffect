from math import trunc
from bs4 import BeautifulSoup
import requests
import os
import json
import dateutil.parser as parser
from datetime import date, datetime, timedelta

from requests.api import head
from requests.models import to_native_string
from requests.sessions import session

# Clear terminal before each run
os.system('cls||clear') # this line clears the screen 'cls' = windows 'clear' = unix

journo_name = "Yuriria-Sierra"

listForJson = []
dateList = []
titleList = []
urlList = []

reqHeader = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

isEnd = False
today = parser.parse("2022-01-10")
while True:
    today = today - timedelta(days=1)

    if((today - parser.parse("2019-12-31")).days > 0):
        jsonData = requests.get(f"https://www.imagentv.com/api/application/news/filter?id=9&date={today.date()}&device=web", headers=reqHeader).json()

        if(len(jsonData)):
            dateList.append(today.isoformat())
            titleList.append(jsonData[0]['title'])
            urlList.append(jsonData[0]['url_desktop'])
    else:
        isEnd == True
        break

# create dict for json
for index, date in enumerate(dateList):
    listForJson.append({"title": titleList[index], "time": date, "author": journo_name, "url": urlList[index]}) 

with open(f"/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/beautifulsoup-kumar/json-files/{journo_name}.json", "a") as f:
    f.write(json.dumps(listForJson, indent=4, ensure_ascii=False))
    f.flush()