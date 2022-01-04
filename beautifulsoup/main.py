import json

from szabolcs_panyi_direkt32_hu import parse_all as parse_szabolcs
from rathod_nihalsing_the_leaflet import parse_all as parse_rathod
from singh_vieta_the_hindu import parse_all as parse_vieta
from the_wire import parse_all as parse_the_wire, json as parse_json
from bradley_hope_wsj import parse_all as parse_bradley
from proceso import parse_all as parse_proceso
from humanite import parse_all as parse_humanite
from quinto_elemento_lab import parse_all as parse_quinto
from matplotlib import pyplot as plt
from datetime import datetime, date
import pandas as pd

def main():
    #
    journalist_name = "Swati Chaturvedi"


    post_data = parse_json("swati-chaturvedi")

    with open(f"{journalist_name.replace(' ', '_').lower()}.json", 'w') as f:
        json.dump(post_data, f, default=json_serial)

    exit(0)


    post_data = pd.read_json(f"{journalist_name.replace(' ', '_').lower()}.json", convert_dates=['time'])
    post_data.set_index('time', inplace=True)

    # date_index = pd.to_datetime(post_data['time'])

    YEAR = 2021

    g = post_data[f'{YEAR}-01-01':f'{YEAR}-12-31']
    g = g['title'].groupby(pd.Grouper(freq='M'))
    print(g)
    g.index.map(lambda dt: dt.month)
    counts = g.count()
    # counts.index = counts.index.map(lambda dt: dt.strftime('%b'))
    print(counts)

    plt.title(f'Posts by {journalist_name} ({YEAR})')
    counts.plot(kind='bar', xlabel=f'Month in {YEAR}', ylabel='# of posts')
    #
    # x = g['title']
    # x.plot()
    #
    # counts['time', 'title'].plot()
    # print(counts)

    # for name, group in times:
    #     print(name)
    #     print(group.sum())
    #
    # sums = times.sum()
    # print(post_data)
    plt.show()
    plt.savefig

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

if __name__ == '__main__':
    main()