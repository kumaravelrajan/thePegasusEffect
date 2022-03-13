import json
import os
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
import cloudscraper

directory = r'C:\Users\kumar\Desktop\TUM\Seminar\pegasus_cybercrime_seminar_latest\json_files'
filenames = ['turan_kislakci_ph']
os.system('clear')

for fileName in filenames:
    with open(directory + f'\\{fileName}.json', 'r', encoding='utf8') as g:
        jsonData = json.load(g)

        for index, jsonRow in enumerate(jsonData):
            #scraper = cloudscraper.create_scraper()
            #html_text = scraper.get(jsonRow['url'])
            html_text = requests.get(jsonRow['url'])
            soup = BeautifulSoup(html_text.text, 'lxml')

            # todo - varies for each website
            articleParas = soup.find('div', class_='news-content').findAll('p')

            for ij, article in enumerate(articleParas):
                articleParas[ij] = article.text

            completeText = ' '.join(articleParas)

            articleLength = completeText.replace('\n', ' ').split(' ')
            jsonRow['length'] = len(articleLength)
            print(index, jsonRow['length'])
            jsonData[index] = jsonRow

        with open(r'C:\Users\kumar\Desktop\TUM\Seminar\pegasus_cybercrime_seminar_latest\Other\beautifulsoup-kumar\jsonWithLength'+ f'\\{fileName}.json', 'w', encoding='utf8') as f:
            json.dump(jsonData, f, indent=4, ensure_ascii=False)
            print('Done')
