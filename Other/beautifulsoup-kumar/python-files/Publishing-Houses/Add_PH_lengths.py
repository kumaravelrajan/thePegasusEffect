import json
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import cloudscraper

directory = '/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/json_files/'
filenames = ['szabolcs_panyi_ph', 'yuriria_sierra_ph', 'eric_bagiruwubusa_ph', 
'vijaita_singh_ph', 'paranjoy_guha_thakurta_ph', 'lenaig_bredoux_ph', 'rafael_rodriguez_castaneda_ph', 'mk_venu_ph', 'turan_kislakci_ph']
os.system('clear')

for fileName in filenames:
    with open(directory + f'{fileName}.json', 'r') as g:
        jsonData = json.load(g)

        for index, jsonRow in enumerate(jsonData):
            #scraper = cloudscraper.create_scraper()
            html_text = requests.get(jsonRow['url'])
            soup = BeautifulSoup(html_text.text, 'lxml')
            print(html_text.text)
            # todo - varies for each website
            articleBody = soup.find('div', class_='cuerpo-nota').findAll('p')
            for index, article in enumerate(articleBody):
                articleBody[index] = article.text

            completeText = ' '.join(articleBody)
            articleLength =  completeText.replace('\n', ' ').split(' ')
            jsonRow['length'] = len(articleLength)
