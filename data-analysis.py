import pandas as pd
import unicodedata
import os
import argparse
import sys
from matplotlib import pyplot as plt

os.system('clear')

def findJournoNameFromFileName(fileName):
    dataSources = ['facebook', 'twitter', 'ph']
    dataSourceFoundInFileName = [dataSource for dataSource in dataSources if dataSource in fileName]
    index = fileName.find('_' + dataSourceFoundInFileName[0])
    filename_base = fileName[:index]
    return filename_base





def main():
    print("{:3} {:3} {:3} {:<}".format('T', 'F', 'P', 'Name'))
    JournosAnalysisFinished = []
    pathToJsonFiles = './json_files/'

    for fileName in os.listdir(pathToJsonFiles):
        if(findJournoNameFromFileName(fileName) not in JournosAnalysisFinished):
            #Find journo name from file name and add journo name to JournosAnalysisFinished so that future needless iterations can be prevented.
            filename_base = findJournoNameFromFileName(fileName)
            JournosAnalysisFinished.append(filename_base)

            twitter = None
            try:
                with open(pathToJsonFiles + filename_base + "_twitter.json") as f:
                    print("{:3} ".format("o"), end='')
                    twitter = pd.read_json(f, convert_dates=['time'])
            except FileNotFoundError:
                print("{:3} ".format('X'), end='')
            facebook = None
            try:
                with open(pathToJsonFiles + filename_base + "_facebook.json") as f:
                    print("{:3} ".format("o"), end='')
                    facebook = pd.read_json(f, convert_dates=['time'])
            except FileNotFoundError:
                print("{:3} ".format('X'), end='')
            publishing_house = None
            try:
                with open(pathToJsonFiles + filename_base + "_ph.json") as f:
                    print("{:3} ".format("o"), end='')
                    publishing_house = pd.read_json(f, convert_dates=['time'])
            except FileNotFoundError:
                print("{:3} ".format('X'), end='')
            print('{:<30}'.format(filename_base))

            aggregated_frames = []
            for frame, suffix in zip([twitter, facebook, publishing_house], ['Twitter', 'Facebook', 'PublishingHouse']):
                if frame is None:
                    aggregated_frames.append(None)
                    continue
                # re-index with time/date as index
                frame.index = frame['time']

                # group by mont
                grouped = frame.groupby(pd.Grouper(freq='1M'))
                print(grouped.head())

                # count new posts per month
                if 'length' in frame:
                    aggregated = grouped.agg(**{f'Count{suffix}': ('time', 'count'), 'AvgLen': ('length', 'mean')})
                else:
                    aggregated = grouped.agg(**{f'Count{suffix}': ('time', 'count')})
                    print(aggregated.head())
                # normalize the datetime to the beginning of the month to allow for easier processing (otherwise it would be
                # the end of the month)
                aggregated.index = aggregated.index.map(lambda dt: dt.replace(day=1, hour=0, minute=0, second=0))
                print(aggregated.head())
                aggregated_frames.append(aggregated)
            all_data = None
            # combine all data points into a single dataframe (inner join, i.e. only months are kept where all three data points exist)
            for agg in aggregated_frames:
                if agg is not None:
                    if all_data is not None:
                        all_data = all_data.join(agg)
                    else:
                        all_data = agg
            if all_data is None:
                continue

            # plot!
            fig, ax = plt.subplots()
            ax2 = ax.twinx() # separate axis for the avg len of articles
            width = 15 # bar width - for some reason this needs to be a really high number
            bottom = None
            # now draw each data series if they exist
            # TODO give the datasets unique colors (e.g. facebook always blue etc)
            # TODO nicer plot formatting
            # TODO maybe limit the time that is plotted to 1-2 years?
            # TODO maybe use an outer join to keep months where there is e.g. facebook data, but no articles published
            if 'CountPublishingHouse' in all_data:
                ax.bar(all_data.index, all_data['CountPublishingHouse'], width)
                bottom = all_data['CountPublishingHouse']
            if 'CountTwitter' in all_data:
                ax.bar(all_data.index, all_data['CountTwitter'], width, bottom=bottom)
                bottom = all_data['CountTwitter']
            if 'CountFacebook' in all_data:
                ax.bar(all_data.index, all_data['CountFacebook'], width, bottom=bottom)
            if 'AvgLen' in all_data:
                ax2.plot(all_data[['AvgLen']].ffill(), color='r', marker='o', ls='-', alpha=.7)
            plt.show()
            pass





if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='process journalist\'s data as json files to generate graphs')
    # parser.add_argument('json', type=argparse.FileType('r'), nargs='+', help='JSON files to read and generate graphs from')
    # args = parser.parse_args()
    main()