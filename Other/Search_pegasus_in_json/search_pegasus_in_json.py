import json
import os
import time

json_directory = 'C:/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/json_files/'
searchPegasus_directory = 'C:/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/Other/Search_pegasus_in_json/pegasus_in_files/'

os.system('clear')

def findJournoNameFromFileName(fileName):
    dataSources = ['facebook', 'twitter', 'ph']
    dataSourceFoundInFileName = [dataSource for dataSource in dataSources if dataSource in fileName]
    index = fileName.find('_' + dataSourceFoundInFileName[0])
    filename_base = fileName[:index]
    return filename_base


# If any files preexisting in searchPegasus_directory delete them all
for fileName in os.listdir(searchPegasus_directory):
    os.remove(searchPegasus_directory + fileName)

# Main
journosAlreadyAnalyzed = []
for fileName in os.listdir(json_directory):
    journoName = findJournoNameFromFileName(fileName)

    if journoName not in journosAlreadyAnalyzed:
        pegasusFoundInPost = []
        journosAlreadyAnalyzed.append(journoName)

        dataSources = ['facebook', 'twitter', 'ph']
        countSourcesWithPegasusKeyword = []

        for dataSource in dataSources:
            try:
                with open(json_directory + journoName + f'_{dataSource}.json', 'r', encoding='utf8') as openFile:
                    print(' -> ' + fileName)
                    jsonData = json.load(openFile)

                    for eachPost in jsonData:
                        if 'pegasus' in eachPost['title'].lower():
                            if(dataSource not in countSourcesWithPegasusKeyword):
                                countSourcesWithPegasusKeyword.append(dataSource)

                            pegasusFoundInPost.append({'time': eachPost['time']})
            except FileNotFoundError:
                continue

        if(len(countSourcesWithPegasusKeyword) >= 2):
            print('Target found')

        if pegasusFoundInPost:
            with open(searchPegasus_directory + findJournoNameFromFileName(fileName) + '_pegasus_search.json', 'a+') as fileToWrite:
                fileToWrite.write(json.dumps(pegasusFoundInPost, indent=4, ensure_ascii=False))
                fileToWrite.flush()

