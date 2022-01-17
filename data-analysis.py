import pandas as pd
import unicodedata
import os
import argparse
import sys
from matplotlib import pyplot as plt

journalists = ["Bradley Hope", "Ferdinand Ayité", "Roula Khalaf", "Khadija Ismayilova", "Taoufik Bouachrine", "Siddharth Varadarajan", "Edwy Plenel", "Szabolcs Panyi", "Yuriria Sierra", "Eric Bagiruwubusa", "Alejandro Patrón", "Carmen Aristegui", "Souleimane Raissouni", "Vijaita Singh", "Paranjoy Guha Thakurta", "Sevinc Vaqifqizi", "Aboubakr Jamai", "Lenaïg Bredoux", "Rafael Rodriguez Castañeda", "MK Venu", "Turan Kışlakçı", "Jaspal Heran", "Rosa Moussaoui", "Maria Moukrim", "Jorge Carrasco", "Swati Chaturvedi", "Alejandro Sicairos", "Smita Sharma", "Hicham Mansouri", "Alejandra Xanic Von Betrab", "Ignacio Cembrero", "Sushant Singh", "Ali Amar", "Marcela Turati", "Carlos Ketohou", "Ricardo Raphael", "Iftikhar Gilani", "Jasur Sumerinli", "Rohini Singh", "David Dercsenyi", "Luis Hernández Navarro", "Alvaro Delgado", "Omar Brouksy"]





def read_files():
    print("{:3} {:3} {:3} {:<}".format('T', 'F', 'P', 'Name'))

    for journalist_name in journalists:
        filename_base = '_'.join(unicodedata.normalize('NFKD', journalist_name.lower().replace('ı', 'i')).encode('ASCII', 'ignore').decode('ASCII').split(' '))
        twitter = None
        # try:
        #     with open(filename_base + "_twitter.json") as f:
        #         print("{:3} ".format("o"), end='')
        #         twitter = pd.read_json(f, convert_dates=['time'])
        # except FileNotFoundError:
        #     print("{:3} ".format('X'), end='')
        facebook = None
        try:
            with open(filename_base + "_facebook.json") as f:
                print("{:3} ".format("o"), end='')
                facebook = pd.read_json(f, convert_dates=['time'])
        except FileNotFoundError:
            print("{:3} ".format('X'), end='')
        publishing_house = None
        try:
            with open(filename_base + "_ph.json") as f:
                print("{:3} ".format("o"), end='')
                publishing_house = pd.read_json(f, convert_dates=['time'])
        except FileNotFoundError:
            print("{:3} ".format('X'), end='')
        print('{:<30} {:<}'.format(journalist_name, filename_base))

        aggregated_frames = []
        for frame in [twitter, facebook, publishing_house]:
            if frame is None:
                aggregated_frames.append(None)
                continue
            # re-index with time/date as index
            frame.index = frame['time']
            # group by mont
            grouped = frame.groupby(pd.Grouper(freq='1M'))
            # count new posts per month
            if 'length' in frame:
                aggregated = grouped.agg(Count=('time', 'count'), AvgLen=('length', 'mean'))
            else:
                aggregated = grouped.agg(Count=('time', 'count'))
            # normalize the datetime to the beginning of the month to allow for easier processing (otherwise it would be
            # the end of the month)
            aggregated.index = aggregated.index.map(lambda dt: dt.replace(day=1, hour=0, minute=0, second=0))
            print(aggregated)
            aggregated_frames.append(aggregated)
        if aggregated_frames[1] is not None and aggregated_frames[2] is not None:
            fig, ax = plt.subplots()
            # plt.hold(True)
            ax2 = ax.twinx()
            all = aggregated_frames[1].join(aggregated_frames[2], lsuffix='Facebook', rsuffix='PublishingHouse')
            if 'AvgLen' in all:
                # plt.hold(True)
                width = 15
                ax.bar(all.index, all['CountPublishingHouse'], width)
                ax.bar(all.index, all['CountFacebook'], width, bottom=all['CountPublishingHouse'])
                # ax.plot(all[['CountPublishingHouse', 'CountFacebook']])
                # ax.plot(all[['AvgLen']])
                ax2.plot(all[['AvgLen']].ffill(), color='r', marker='o', ls='-', alpha=.7)
                plt.show()
                pass
            else:
                continue





if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='process journalist\'s data as json files to generate graphs')
    # parser.add_argument('json', type=argparse.FileType('r'), nargs='+', help='JSON files to read and generate graphs from')
    # args = parser.parse_args()
    read_files()