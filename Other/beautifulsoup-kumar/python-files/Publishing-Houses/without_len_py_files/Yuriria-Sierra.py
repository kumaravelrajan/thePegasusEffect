from math import trunc
from bs4 import BeautifulSoup
import requests
import os
import json
import dateutil.parser as parser
import datetime

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

offset = 0
isEnd = False

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}


while True:
    reqSession = requests.session()
    jsonData = reqSession.get(f'https://api.imagendigital.com/v2/excelsior/nodes.json/339fd1e0444ddbbd4d4528d8df161108?limit=12&type=blog&columnist.uid=574&sort=created:DESC&offset={offset}', headers=headers).json()
    print(jsonData)

    articlesList = jsonData['data']

    for article in articlesList:
        createdDate = datetime.datetime.fromtimestamp(article['created'])  
        if((createdDate - parser.parse("2019-12-31")).days > 0):
            dateList.append(createdDate.isoformat())
            titleList.append(article['title'])
            urlList.append(article['url'])
        else:
            isEnd = True
            break
    
    if(isEnd):
        break
    else:
        offset += 12

# create dict for json
for index, date in enumerate(dateList):
    listForJson.append({"title": titleList[index], "time": date, "author": journo_name, "url": urlList[index]}) 

with open(f"/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/beautifulsoup-kumar/json-files/{journo_name}.json", "w") as f:
    f.write(json.dumps(listForJson, indent=4, ensure_ascii=False))
    f.flush()

# https://api.imagendigital.com/v2/excelsior/nodes.json/339fd1e0444ddbbd4d4528d8df161108?limit=12&type=blog&columnist.uid=574&sort=created:DESC&offset=0
# https://api.imagendigital.com/v2/excelsior/nodes.json/339fd1e0444ddbbd4d4528d8df161108?limit=12&type=blog&columnist.uid=574&sort=created:DESC&offset=12