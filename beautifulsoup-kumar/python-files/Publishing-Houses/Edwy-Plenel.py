from bs4 import BeautifulSoup
import requests
import os
import json
import dateutil.parser as parser

from requests.api import head

# todo - page 2

# Clear terminal before each run
os.system('cls||clear') # this line clears the screen 'cls' = windows 'clear' = unix

journo_name = "Edwy-Plenel"
listForToWriteToJson = []
for j in range(1,3):
    html_text = requests.get(f"https://www.mediapart.fr/en/biographie/edwy-plenel?page={j}")
    soup = BeautifulSoup(html_text.text, 'lxml')

    allArticles = soup.find_all("li" , attrs={"data-type":"article"})   

    dates = []
    links = []
    headings = []

    # dates
    for i in allArticles:
        # dates.append(i.find('time')['datetime'])
        dates.append((parser.parse(i.find('time')['datetime'])).isoformat())

    # links
    for i in allArticles:
        links.append(f"https://www.mediapart.fr{i.find('h3', class_ = 'title').a['href']}")

    # headings
    for i in allArticles:
        headings.append(i.find('h3', class_ = "title").text.strip())

    # create dict for json
    for index, date in enumerate(dates):
        tempdict = {"title": headings[index], "time": date, "author": journo_name, "url": links[index]}#, “length”: $length_in_words}
        listForToWriteToJson.append(tempdict)

print(os.system("ls ../json-files/"))
with open(f"/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/beautifulsoup-kumar/json-files/{journo_name}.json", "w") as f:
    f.write(json.dumps(listForToWriteToJson, indent=4, ensure_ascii=False))
    f.flush()