from bs4 import BeautifulSoup
import requests
import os
import json
import dateutil.parser as parser

from requests.api import head

# Clear terminal before each run
os.system('cls||clear') # this line clears the screen 'cls' = windows 'clear' = unix

journo_name = "Szabolcs-Panyi"

listForJson = []

for j in range(1,3):
    html_text = requests.get(f"https://www.direkt36.hu/en/author/szabolcs/page/{j}/")
    soup = BeautifulSoup(html_text.text, 'lxml')

    datesList = []
    titlesList = []
    urls = []

    # Collect all dates
    dates = soup.findAll('time', class_="entry-date")
    for date in dates:
        datesList.append(parser.parse(date.text).isoformat())

    # Collect all titles and urls
    titles = soup.findAll('h1', class_="entry-title")
    for title in titles:
        urls.append(title.a['href'])
        titlesList.append(title.text)

    # create dict for json
    for index, date in enumerate(datesList):
        listForJson.append({"title": titlesList[index], "time": date, "author": journo_name, "url": urls[index]}) 

with open(f"/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/beautifulsoup-kumar/json-files/{journo_name}.json", "w") as f:
    f.write(json.dumps(listForJson, indent=4, ensure_ascii=False))
    f.flush()