import requests
from bs4 import BeautifulSoup
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd


URLS = ["https://www.direkt36.hu/hu/author/szabolcs/", "https://www.direkt36.hu/author/szabolcs/page/2/", "https://www.direkt36.hu/author/szabolcs/page/3/"]

def parse_article(url):
    print('parsing url', url)
    res = requests.get(url)
    assert res.status_code == 200
    soup = BeautifulSoup(res.text)
    time = soup.find('time', class_='entry-date')
    print(time.get('datetime'))


def main():
    post_data = []
    for URL in URLS:
        res = requests.get(URL)
        assert res.status_code == 200
        soup = BeautifulSoup(res.text)
        posts = soup.find_all('h1', class_='entry-title')
        for post in posts:
            title = post.contents[0].string
            url = post.contents[0].get('href')
            time = post.parent.find_next_sibling('article').find(class_='entry-date').find('time').get('datetime')
            time = datetime.fromisoformat(time)

            post_data.append({
                'title': title,
                'url': url,
                'time': time,
            })

    print(len(post_data))
    print(post_data)
    times = list(map(lambda post: post['time'], post_data))
    dates = matplotlib.dates.date2num(times)
    print(dates)

    fig, ax = plt.subplots()
    ax.eventplot(times, orientation='horizontal')

    plt.show()





if __name__ == '__main__':
    main()