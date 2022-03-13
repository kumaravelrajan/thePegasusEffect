import json
import os
import pandas as pd

directory = '/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/json_files/'
directoryToStoreAt = '/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/json_files_changeFormat/'
os.system('clear')

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if 'twitter' in filename: 
        jsonDataDict = []

         # print(os.path.join(directory, filename))
        tweets_df = pd.read_json(directory + filename, lines=True)

        for index, row in tweets_df.iterrows():
            print(tweets_df.iloc[index])
            jsonDataDict.append({'title':tweets_df.iloc[index]['content'], 'time': tweets_df.iloc[index]['date'].isoformat(), 
            'author': tweets_df.iloc[index]['user']['username'],'url': tweets_df.iloc[index]['url']})

        #jsonDataDict now has all the data to be stored in the json file. Dump this into the correctly named json file.
        with open(directoryToStoreAt + filename, 'w') as f:
            f.write(json.dumps(jsonDataDict, indent=4, ensure_ascii=False))
            f.flush()