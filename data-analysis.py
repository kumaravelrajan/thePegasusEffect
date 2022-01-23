import datetime

import numpy
import pandas as pd
import unicodedata
import os
import argparse
import sys
from matplotlib import pyplot as plt
import numpy as np

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

    # Not all journos data can be analyzed in the period jan 2020 to dec 2021.
    # Some have different timelines. Specifying the last date when their posts are not important for analysis for such journos so that they can be dropped from the table.
    # todo - daniel to add names and dates.
    irrelevantDatesForJournoAnalysis = {
        'taoufik_bouachrine': '2017-12-31',
        'carmen_aristegui' : '2016-12-31',
        'paranjoy_guha_thakurta' : '2018-12-31'
    }

    for fileName in os.listdir(pathToJsonFiles):
        if(findJournoNameFromFileName(fileName) not in JournosAnalysisFinished):
            #Find journo name from file name and add journo name to JournosAnalysisFinished so that future needless iterations can be prevented.
            filename_base = findJournoNameFromFileName(fileName)
            JournosAnalysisFinished.append(filename_base)

            twitter = None
            try:
                with open(pathToJsonFiles + filename_base + "_twitter.json", encoding='utf8') as f:
                    print("{:3} ".format("o"), end='')
                    twitter = pd.read_json(f, convert_dates=['time'])
            except FileNotFoundError:
                print("{:3} ".format('X'), end='')
            facebook = None
            try:
                with open(pathToJsonFiles + filename_base + "_facebook.json", encoding='utf8') as f:
                    print("{:3} ".format("o"), end='')
                    facebook = pd.read_json(f, convert_dates=['time'])
            except FileNotFoundError:
                print("{:3} ".format('X'), end='')
            publishing_house = None
            try:
                with open(pathToJsonFiles + filename_base + "_ph.json", encoding='utf8') as f:
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
                frame.index = frame['time'].dt.tz_localize(None)

                # group by month
                grouped = frame.groupby(pd.Grouper(freq='1M'))

                # count new posts per month
                if 'length' in frame:
                    aggregated = grouped.agg(**{f'Count{suffix}': ('time', 'count'), 'AvgLen': ('length', 'mean')})
                else:
                    aggregated = grouped.agg(**{f'Count{suffix}': ('time', 'count')})
                # normalize the datetime to the beginning of the month to allow for easier processing (otherwise it would be
                # the end of the month)
                aggregated.index = aggregated.index.map(lambda dt: dt.replace(day=1, hour=0, minute=0, second=0))
                aggregated_frames.append(aggregated)
            all_data = None
            # combine all data points into a single dataframe (inner join, i.e. only months are kept where all three
            # data points exist)
            for agg in aggregated_frames:
                if agg is not None:
                    if all_data is not None:
                        all_data = all_data.join(agg, how='outer')
                    else:
                        all_data = agg
            if all_data is None:
                continue

            # plot!
            # Note: There is a bug with pandas when it comes to plotting with DataFrame.plot and datetime indexes
            # For this reason we are plotting directly with pyplot.
            # See: https://github.com/pandas-dev/pandas/issues/10761
            fig, ax = plt.subplots()
            fig.set_size_inches(18.5, 10.5)
            width = 15 # bar width - for some reason this needs to be a really high number
            bottom = []

            # Drop irrelevant date ranges. Default - start from Jan 1, 2020.
            endDate = datetime.time(0,0,0)
            if(filename_base in irrelevantDatesForJournoAnalysis):
                endDate = pd.to_datetime(irrelevantDatesForJournoAnalysis[filename_base])
            else:
                endDate = pd.to_datetime('2019-12-31')

            all_data = all_data.drop(pd.date_range(start=all_data.index[0], end=endDate), errors='ignore')

            # replace nan with 0.0
            np.nan_to_num(all_data, False, 0.0)

            p1, p2, p3 = 0, 0, 0
            # now draw each data series if they exist
            if 'CountPublishingHouse' in all_data:
                p1 = ax.bar(all_data.index, all_data['CountPublishingHouse'], width, color='green')
                bottom = numpy.array(all_data['CountPublishingHouse'])
                numpy.nan_to_num(bottom, copy=False,nan=0.0)
            else:
                bottom = np.zeros(len(all_data.index))

            if 'CountTwitter' in all_data:
                p2 = ax.bar(all_data.index, all_data['CountTwitter'], width, bottom=bottom, color='dodgerblue')
                bottom += numpy.array(all_data['CountTwitter'])
                numpy.nan_to_num(bottom, nan=0.0)

            if 'CountFacebook' in all_data:
                p3 = ax.bar(all_data.index, all_data['CountFacebook'], width, bottom=bottom, color='darkblue')

            if 'AvgLen' in all_data:
                ax2 = ax.twinx()  # separate axis for the avg len of articles
                ax2.plot(all_data[['AvgLen']].ffill(), color='r', marker='o', ls='-', alpha=.7)

            ax.set_xlabel('TIME')
            ax.set_ylabel('#POSTS')

            #xtickDf = all_data.index.strftime('%b-%Y').to_frame()
            #ax.set_xticks(ticks = range(0, len(xtickDf.index)), labels = xtickDf.index, rotation=45)
            plt.title(f'Analysis of {filename_base}')

            headers = []
            plots = []

            if(p1):
                plots.append(p1[0])
                headers.append('PublishingHouse')
            if(p2):
                plots.append(p2[0])
                headers.append('Twitter')
            if(p3):
                plots.append(p3[0])
                headers.append('Facebook')

            plt.legend(plots, headers)

            #plt.ylim([0, (max(all_data['CountPublishingHouse'].array + all_data['CountFacebook'].array + all_data['CountTwitter'].array) + 200) ])
            plt.show()
            pass





if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='process journalist\'s data as json files to generate graphs')
    # parser.add_argument('json', type=argparse.FileType('r'), nargs='+', help='JSON files to read and generate graphs from')
    # args = parser.parse_args()
    main()