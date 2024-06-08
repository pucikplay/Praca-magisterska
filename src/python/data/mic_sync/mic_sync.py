import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import ConnectionPatch

NODES_NO = 4
labels = ['0', '1', '2', '3']
colors = ['r', 'g', 'b', 'y']


def plot_offsets(df, name, ylim):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    ax[0].ticklabel_format(style='plain')
    ax[1].ticklabel_format(style='plain')

    for i in range(NODES_NO):
        df.plot(x='row_number', y=labels[i], color=colors[i], label=f"Węzeł {i}", kind='scatter', s=5, ax=ax[0])
    # plt.title("Przesunięcie zegarów")
    ax[0].set_xlabel("Numer testu")
    ax[0].set_ylabel("Czas [us]")
    ax[0].legend()

    ax[1].set_ylim(ylim)

    for i in range(NODES_NO):
        df.plot(x='row_number', y=labels[i], color=colors[i], label=f"Węzeł {i}", kind='scatter', s=5, ax=ax[1])
    # plt.title("Przesunięcie zegarów")
    ax[1].set_xlabel("Numer testu")
    ax[1].set_ylabel("Czas [us]")
    ax[1].legend()

    y_min, y_max = ylim
    ax[0].axhline(y=y_min, color='red', linestyle='--', xmin=ax[0].get_xlim()[0], xmax=ax[0].get_xlim()[1])
    ax[0].axhline(y=y_max, color='red', linestyle='--', xmin=ax[0].get_xlim()[0], xmax=ax[0].get_xlim()[1])

    con = ConnectionPatch(xyA=(ax[0].get_xlim()[1], y_min), xyB=(ax[1].get_xlim()[0], y_min), coordsA="data", coordsB="data", axesA=ax[0], axesB=ax[1], color="red", linestyle='--')
    fig.add_artist(con)
    con = ConnectionPatch(xyA=(ax[0].get_xlim()[1], y_max), xyB=(ax[1].get_xlim()[0], y_max), coordsA="data", coordsB="data", axesA=ax[0], axesB=ax[1], color="red", linestyle='--')
    fig.add_artist(con)

    fig.tight_layout()
    plt.savefig(f'../../charts/mic_sync/{name}.png', dpi=300)
    plt.close()

def plot_stddevs(df):
    stddevs = {x: df.std()[x] for x in labels}

    plt.bar(*zip(*stddevs.items()))
    # plt.title("Odchylenia standardowe przesunięć")
    plt.xlabel("Numer węzła")
    plt.ylabel("Odchylenie [us]")
    plt.tight_layout()
    plt.savefig(f'../../charts/mic_sync/stddev_offsets.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    df = pd.read_csv('mic_sync.csv')
    df = df.drop([0])
    df.reset_index(drop=True, inplace=True)
    df = df.assign(row_number=range(len(df)))

    df[labels] -= df[labels].mean()

    plot_offsets(df, 'offsets', (-150, 150))
    plot_stddevs(df)