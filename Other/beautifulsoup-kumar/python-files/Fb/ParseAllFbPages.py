from facebook_scraper import *
from math import trunc
from bs4 import BeautifulSoup
from facebook_scraper.fb_types import Page
import requests
import os
import json
import dateutil.parser as parser
from datetime import date, datetime, timedelta
from requests import cookies
import os

os.system('clear')
listForJson = []

dict_Name_Fb = {
    # 'icembrero': 'ignacia_cembrero',
    # 'ali.amar.585559' : 'ali_amar',
    # 'ricardomraphael' : 'ricardo_raphael',
    # 'iftikhar.gilani' : 'iftikar_ghilani',
    # 'cesur.sumerinli' : 'jasur_sumerinli',
    # 'SmitaSharmaJournalist' : 'smita_sharma',
    'alejandro.sicairosrivas' : 'alejandro_sicairos'#,
    #'maria.moukrim' : 'maria_moukrim'
}

# Scrape Facebook for posts
temporary_banned_count = 0
dateExceed = 0
startDateExceedCalculation = False

for index, dictKey in enumerate(dict_Name_Fb):
    try:
        for post in get_posts(dictKey, pages=2000 , options={"allow_extra_requests": False, "posts_per_page": 200},  
        cookies="/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/Other/beautifulsoup-kumar/python-files/Fb/cookies.json"):
            try:
                ctDate = parser.parse(post['time'].strftime("%Y-%m-%d"))
                if((parser.parse(post['time'].strftime("%Y-%m-%d")) - parser.parse("2016-12-31")).days > 0):
                    listForJson.append({"title": post['post_text'], "time": post['time'].isoformat(), "author": dict_Name_Fb[dictKey], "url": post['post_url']})

                    if(startDateExceedCalculation):
                        startDateExceedCalculation = False
                        dateExceed = 0
                else:
                    # When post date before 2019 dec 31 we come here.Then, check if genuinely date preceeded or a shared post has a prior date.
                    # startDateExceedCalculation set to true here. 
                    if(not startDateExceedCalculation):
                        startDateExceedCalculation = True

                    # 
                    if(startDateExceedCalculation):
                        dateExceed += 1
                    if(dateExceed > 5):
                        break
            except:
                continue

        with open(f"/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/json_files/" + dict_Name_Fb[dictKey] + '_facebook.json', "w") as f:
            f.write(json.dumps(listForJson, indent=4, ensure_ascii=False))
            f.flush()
    except exceptions.TemporarilyBanned as e:
        temporary_banned_count += 1
        sleep_secs = 600 * temporary_banned_count
        time.sleep(sleep_secs)
