from bs4 import BeautifulSoup
import requests
import os
import json

# Clear terminal before each run
os.system('cls||clear') # this line clears the screen 'cls' = windows 'clear' = unix

journo_name = "roula-khalaf"
listForToWriteToJson = []
for i in range(1,3):
    html_text = requests.get(f'https://www.ft.com/roula-khalaf?page={i}')
    soup =  BeautifulSoup(html_text.text, 'lxml')
    all_posts_all_tags = soup.find_all("li", class_ = "o-teaser-collection__item o-grid-row")
    all_visible_dates = soup.find_all(class_ = "stream-card__date")
    all_headings = soup.find_all(class_ = "o-teaser__heading")
    all_links = []
    
    for i in all_headings:
        all_links.append(f"https://www.ft.com{i.a['href']}")

    for index, date in enumerate(all_visible_dates):
        tempdict = {"title": all_headings[index].text, "time": date.text.strip('\n'), "author": journo_name, "url": all_links[index]}#, “length”: $length_in_words}
        listForToWriteToJson.append(tempdict)

with open(f"json-files/{journo_name}.json", "w") as f:
    f.write(json.dumps(listForToWriteToJson, indent=4, ensure_ascii=False))
    f.flush()