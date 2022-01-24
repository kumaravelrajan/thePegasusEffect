import json
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import cloudscraper

directory = r'C:\Users\kumar\Desktop\TUM\Seminar\pegasus_cybercrime_seminar_latest\json_files'
filenames = ['szabolcs_panyi_ph', 'yuriria_sierra_ph', 'eric_bagiruwubusa_ph',
'vijaita_singh_ph', 'paranjoy_guha_thakurta_ph', 'lenaig_bredoux_ph', 'rafael_rodriguez_castaneda_ph', 'mk_venu_ph', 'turan_kislakci_ph']
os.system('clear')

for fileName in filenames:
    with open(directory + f'\\{fileName}.json', 'r', encoding='utf8') as g:
        jsonData = json.load(g)

        for index, jsonRow in enumerate(jsonData):
            #scraper = cloudscraper.create_scraper()
            html_text = requests.get(jsonRow['url'])
            soup = BeautifulSoup(html_text.text, 'lxml')

            # todo - varies for each website
            articleParas = soup.find('div', class_='entry-content').findAll('p')
            articleHeadings = soup.find('div', class_='entry-content').findAll('h2')

            for ij, article in enumerate(articleParas):
                articleParas[ij] = article.text

            for ij, article in enumerate(articleHeadings):
                articleHeadings[ij] = article.text


            completeText = ' '.join(articleParas)
            completeText += ' '.join(articleHeadings)

            articleLength =  completeText.replace('\n', ' ').split(' ')
            jsonRow['length'] = len(articleLength)
            print(index, jsonRow['length'])
            jsonData[index] = jsonRow

        g.seek(0)
        with open(r'C:\Users\kumar\Desktop\TUM\Seminar\pegasus_cybercrime_seminar_latest\Other\beautifulsoup-kumar\jsonWithLength'+ f'\\{fileName}.json', 'w', encoding='utf8') as f:
            json.dump(jsonData, f, indent=4, ensure_ascii=False)
            print('Done')
