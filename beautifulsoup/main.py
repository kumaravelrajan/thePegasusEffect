from szabolcs_panyi_direkt32_hu import parse_all as parse_szabolcs
from matplotlib import pyplot as plt

def main():
    post_data = parse_szabolcs()
    times = list(map(lambda post: post['time'], post_data))


    fig, ax = plt.subplots()
    plt.xticks(rotation=45)
    ax.eventplot(times, orientation='horizontal')

    plt.show()

if __name__ == '__main__':
    main()