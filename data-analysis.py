import datetime

import numpy
import pandas as pd
import unicodedata
import os
import argparse
import sys
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import numpy as np

os.system('clear')

WINDOW_SIZE = 12 # in months

def findJournoNameFromFileName(fileName):
    dataSources = ['facebook', 'twitter', 'ph', 'pegasus_search']
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
    irrelevantDatesForJournoAnalysis = {
        'taoufik_bouachrine': '2017-12-31',
        'carmen_aristegui' : '2016-12-31',
        'paranjoy_guha_thakurta' : '2018-12-31',
        'alejandro_sicairos' : '2016-12-31',
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
            pegasus_mentions = None
            try:
                with open(pathToJsonFiles + filename_base + "_pegasus_search.json", encoding='utf8') as f:
                    pegasus_mentions = pd.read_json(f, convert_dates=['time'])
                    pegasus_mentions['time'] = pd.to_datetime(pegasus_mentions['time'], utc=True)
                    pegasus_mentions.index = pegasus_mentions['time'].dt.tz_localize(None)
                    pegasus_mentions = pegasus_mentions['time']
            except FileNotFoundError:
                pass

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

            # also join in the data of pegasus mentions
            if pegasus_mentions is not None:
                grouped = pegasus_mentions.groupby(pd.Grouper(freq='1M'))
                aggregated = grouped.agg(**{'PegasusMentions': 'count'})
                aggregated.index = aggregated.index.map(lambda dt: dt.replace(day=1, hour=0, minute=0, second=0))
                aggregated_frames.append(aggregated)
                pass


            all_data = None
            # combine all data points into a single dataframe (outer join)
            for agg in aggregated_frames:
                if agg is not None:
                    if all_data is not None:
                        all_data = all_data.join(agg, how='outer')
                    else:
                        all_data = agg
            if all_data is None:
                continue

            # Set the count values to all be float64 (due to the join, they might get converted to float64s to represent
            # NaN values). floats don't hurt our case, and we need all values to be the same type
            for column in ['CountTwitter', 'CountFacbook', 'CountPublishingHouse']:
                if column in all_data:
                    all_data[column] = all_data[column].astype('float64')

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

            # replace nan with 0.0 (except for AvgLen)
            col_list = list(all_data)
            if 'AvgLen' in col_list:
                col_list.remove('AvgLen')
            values = {}
            for c in col_list:
                values[c] = 0.0
            all_data.fillna(value=values, inplace=True)

            p1, p2, p3, p4 = 0, 0, 0, 0
            # now draw each data series if they exist
            numOfArticles = np.zeros(len(all_data.index))
            avgLenOfArticles = np.zeros(len(all_data.index))

            col_list = list(all_data)
            if 'AvgLen' in col_list:
                col_list.remove('AvgLen')
            if 'PegasusMentions' in col_list:
                col_list.remove('PegasusMentions')
            all_data['CountTotal'] = all_data[col_list].sum(axis=1)
            windowed_mean = all_data['CountTotal'].rolling(WINDOW_SIZE, min_periods=1).mean()
            if 'CountPublishingHouse' in all_data:
                p1 = ax.bar(all_data.index, all_data['CountPublishingHouse'], width, color='green')
                bottom = numpy.array(all_data['CountPublishingHouse'])
                numpy.nan_to_num(bottom, copy=False,nan=0.0)
                numOfArticles += all_data['CountPublishingHouse'].array
            else:
                bottom = np.zeros(len(all_data.index))

            if 'CountTwitter' in all_data:
                p2 = ax.bar(all_data.index, all_data['CountTwitter'], width, bottom=bottom, color='dodgerblue')
                bottom += numpy.array(all_data['CountTwitter'])
                numpy.nan_to_num(bottom, nan=0.0)
                numOfArticles += all_data['CountTwitter'].array

            if 'CountFacebook' in all_data:
                p3 = ax.bar(all_data.index, all_data['CountFacebook'], width, bottom=bottom, color='darkblue')
                numOfArticles += all_data['CountFacebook'].array

            if 'AvgLen' in all_data:
                ax2 = ax.twinx()  # separate axis for the avg len of articles
                p4 = ax2.plot(all_data[['AvgLen']].dropna(), color='r', marker='o', ls='-', alpha=.7)
                avgLenOfArticles = np.nan_to_num(all_data['AvgLen'].array, False)
                ax2.set_ylabel('Avg. article length')
                ax2.set_ylim(0, max(avgLenOfArticles) + 15)

            if 'PegasusMentions' in all_data:
                p5 = ax.bar(all_data.index, all_data['PegasusMentions'], width // 4, color='r')

            # plot rolling average
            rolling_avg = ax.plot(all_data.index, windowed_mean, color='darkblue', linestyle='dashed')

            ax.set_xlabel('TIME')
            ax.set_ylabel('#POSTS')

            ax.set_xticks(all_data.index)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))
            ax.tick_params(axis='x', which='both', rotation=45)

            plt.title(f'Analysis of {" ".join(map(lambda s: s.capitalize(), filename_base.split("_")))}')

            # Legend
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
            if(p4):
                plots.append(p4[0])
                headers.append('Avg. article length')
            if(p5):
                plots.append(p5[0])
                headers.append('Mentions of keyword "pegasus"')

            plots.append(rolling_avg[0])
            headers.append(f'{WINDOW_SIZE}-month rolling avg. of total contribution count')

            plt.legend(plots, headers)

            # set y axis limit
            ax.set_ylim(0,max(numOfArticles) + 15)

            # plt.show() # TODO remove
            plt.savefig(f'./graphs/{filename_base}.png', dpi=fig.dpi)
            pass





if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='process journalist\'s data as json files to generate graphs')
    # parser.add_argument('json', type=argparse.FileType('r'), nargs='+', help='JSON files to read and generate graphs from')
    # args = parser.parse_args()
    main()
