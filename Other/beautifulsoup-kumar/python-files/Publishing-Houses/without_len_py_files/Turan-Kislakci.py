from bs4 import BeautifulSoup
import requests
import os
import json
import dateutil.parser as parser

from requests.api import head

# Clear terminal before each run
os.system('cls||clear') # this line clears the screen 'cls' = windows 'clear' = unix

journo_name = "Turan-Kislakci"

listForJson = []
dateList = []
titleList = []
urlList = []

turkishToEnglishMonths = {'ocak':'January', 'şubat':'February', 'mart':'March', 'nisan':'April', 'mayıs':'May', 'haziran':'June', 'temmuz':'July'
, 'ağustos':'August', 'eylül':'September', 'ekim':'October', 'kasım':'November', 'aralık':'December'}

for pageCounter in range(1,7):
    html_text = requests.get(f"https://www.istiklal.com.tr/yazar/turan-kislakci?sayfa={pageCounter}")
    soup = BeautifulSoup(html_text.text, 'lxml')

    ParentElementsList = soup.find('div', class_='article-list').findAll('figure')

    for parentElement in ParentElementsList:
        titleList.append(parentElement.figcaption.a['title'])
        urlList.append(parentElement.figcaption.a['href'])

        #date
        turkishDate = parentElement.find('span', class_='info').text.split()
        turkishDate[1] = turkishToEnglishMonths[turkishDate[1].lower()]
        dateList.append(parser.parse(' '.join(turkishDate[:-1])).isoformat())
        # dateList.append()

# create dict for json
for index, date in enumerate(dateList):
    listForJson.append({"title": titleList[index], "time": date, "author": journo_name, "url": urlList[index]}) 

with open(f"/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/beautifulsoup-kumar/json-files/{journo_name}.json", "w") as f:
    f.write(json.dumps(listForJson, indent=4, ensure_ascii=False))
    f.flush()