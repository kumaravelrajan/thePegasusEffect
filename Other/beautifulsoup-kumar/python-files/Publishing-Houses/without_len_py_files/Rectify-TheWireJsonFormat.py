import json

fileNames = ['/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/News-Outlet-Analysis/mk_venu.json', 
'/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/News-Outlet-Analysis/siddhart_varadarajan.json', 
'/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/News-Outlet-Analysis/vijaita_singh.json']

journo_name = ['mk_venu', 'siddhart_varadarajan', 'vijaita_singh']

for index, fileName in enumerate(fileNames):
    with open(fileName, "r") as g:
        jsonData = json.load(g)

    with open(f"/mnt/c/Users/kumar/Desktop/TUM/Seminar/pegasus_cybercrime_seminar_latest/beautifulsoup-kumar/json-files/Publishing-Houses/{journo_name[index]}.json", "w") as f:
        f.write(json.dumps(jsonData, indent=4, ensure_ascii=False))
        f.flush()