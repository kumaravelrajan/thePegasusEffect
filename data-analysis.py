import pandas as pd
import unicodedata
import os
import argparse
import sys

journalists = ["Bradley Hope", "Ferdinand Ayité", "Roula Khalaf", "Khadija Ismayilova", "Taoufik Bouachrine", "Siddharth Varadarajan", "Edwy Plenel", "Szabolcs Panyi", "Yuriria Sierra", "Eric Bagiruwubusa", "Alejandro Patrón", "Carmen Aristegui", "Souleimane Raissouni", "Vijaita Singh", "Paranjoy Guha Thakurta", "Sevinc Vaqifqizi", "Aboubakr Jamai", "Lenaïg Bredoux", "Rafael Rodriguez Castañeda", "MK Venu", "Turan Kışlakçı", "Jaspal Heran", "Rosa Moussaoui", "Maria Moukrim", "Jorge Carrasco", "Swati Chaturvedi", "Alejandro Sicairos", "Smita Sharma", "Hicham Mansouri", "Alejandra Xanic Von Betrab", "Ignacio Cembrero", "Sushant Singh", "Ali Amar", "Marcela Turati", "Carlos Ketohou", "Ricardo Raphael", "Iftikhar Gilani", "Jasur Sumerinli", "Rohini Singh", "David Dercsenyi", "Luis Hernández Navarro", "Alvaro Delgado", "Omar Brouksy"]





def check_journalist_files():
    print("{:3} {:3} {:3} {:<}".format('T', 'F', 'P', 'Name'))
    for journalist_name in journalists:
        filename_base =  '_'.join(unicodedata.normalize('NFKD', journalist_name.lower().replace('ı', 'i')).encode('ASCII', 'ignore').decode('ASCII').split(' '))
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
        # frame = pd.read_json(f)
        # print(frame)



if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='process journalist\'s data as json files to generate graphs')
    # parser.add_argument('json', type=argparse.FileType('r'), nargs='+', help='JSON files to read and generate graphs from')
    # args = parser.parse_args()
    check_journalist_files()