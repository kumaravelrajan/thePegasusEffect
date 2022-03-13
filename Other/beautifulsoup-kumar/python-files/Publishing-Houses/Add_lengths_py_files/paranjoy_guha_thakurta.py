import json
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import cloudscraper

directory = r'C:\Users\kumar\Desktop\TUM\Seminar\pegasus_cybercrime_seminar_latest\json_files'
filenames = ['paranjoy_guha_thakurta_ph', 'lenaig_bredoux_ph', 'rafael_rodriguez_castaneda_ph', 'mk_venu_ph', 'turan_kislakci_ph']
os.system('clear')

for fileName in filenames:
    with open(r'/Other/beautifulsoup-kumar/json-files/Publishing-Houses/paranjoy_guha_thakurta_withoutLen.json', 'r', encoding='utf8') as g:
        jsonData = json.load(g)

        for index, jsonRow in enumerate(jsonData):
                #scraper = cloudscraper.create_scraper()
                #html_text = scraper.get(jsonRow['url'])
                if '/video/' not in jsonRow['url']:
                    html_text = requests.get(jsonRow['url'])
                    soup = BeautifulSoup(html_text.text, 'lxml')

                    # todo - varies for each website
                    articleParas = soup.find('article').findAll('p')

                    for ij, article in enumerate(articleParas):
                        articleParas[ij] = article.text

                    completeText = ' '.join(articleParas)

                    articleLength =  completeText.replace('\n', ' ').split(' ')
                    jsonRow['length'] = len(articleLength)
                    print(index, jsonRow['length'])
                    jsonData[index] = jsonRow
                else:
                    break

        with open(r'C:\Users\kumar\Desktop\TUM\Seminar\pegasus_cybercrime_seminar_latest\Other\beautifulsoup-kumar\json-files\paranjoy_guha_thakurta_withLen.json', 'w', encoding='utf8') as f:
            json.dump(jsonData, f, indent=4, ensure_ascii=False)
            print('Done')
