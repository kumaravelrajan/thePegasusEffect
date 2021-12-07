from szabolcs_panyi_direkt32_hu import parse_all as parse_szabolcs
from rathod_nihalsing_the_leaflet import parse_all as parse_rathod
from singh_vieta_the_hindu import parse_all as parse_vieta
from matplotlib import pyplot as plt
from datetime import datetime, date
import pandas as pd

def main():
    # post_data = parse_vieta()
    #
    # print(post_data)

    post_data = pd.read_json('vieta_2.json', convert_dates=['time'])

    # date_index = pd.to_datetime(post_data['time'])

    g = post_data.groupby(pd.Grouper(key='time', freq='M'))
    counts = g.count()

    counts.unstack().plot(kind='bar')
    print(counts)

    # for name, group in times:
    #     print(name)
    #     print(group.sum())
    #
    # sums = times.sum()
    # print(post_data)
    # plt.show()

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

if __name__ == '__main__':
    main()