import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import ConnectionPatch

NODES_NO = 4
labels = [str(i) for i in range(NODES_NO)]
colors = ['r', 'g', 'b', 'y']


def plot_data(df, no):
    fig, ax = plt.subplots()

    for i in range(NODES_NO):
        df.plot(x='row_number', y=labels[i], color=colors[:NODES_NO][i], label=f"Node {i}", kind='scatter', s=5, ax=ax)
    
    plt.title("Message transit time")
    plt.xlabel("Message no.")
    plt.ylabel("Time [us]")
    plt.legend()
    plt.savefig(f"../../charts/mtt/mtt_{no}.png", dpi=300)

    df.hist(column=labels, bins=range(0,5000,300))
    
    plt.title("Message transit time")
    plt.xlabel("Message no.")
    plt.ylabel("Time [us]")
    plt.legend()
    plt.savefig(f"../../charts/mtt/mtt_bar_{no}.png", dpi=300)

    fig, ax = plt.subplots()

    for i in range(1,NODES_NO):
        df.plot(x='row_number', y=f'{labels[i]}_delta', color=colors[i], label=f"Node {i}", ax=ax)

    plt.title("Message transit time deltas")
    plt.xlabel("Message no.")
    plt.ylabel("Time [us]")
    plt.legend()
    plt.savefig(f"../../charts/mtt/mtt_delta_{no}.png", dpi=300)
    
def plot_deltas(df):
    df.plot.bar()
    plt.title("Message transit time deltas means")
    plt.xlabel("Test no.")
    plt.ylabel("Time [us]")
    plt.legend()
    plt.savefig(f"../../charts/mtt/mtt_deltas_means.png", dpi=300)

def plot_offsets(df, name, ylim):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    for i in range(NODES_NO):
        df.plot(x='row_number', y=labels[i], color=colors[i], label=f"Węzeł {i}", kind='scatter', s=5, ax=ax[0])
    # ax[0].title("Przesunięcie zegarów")
    ax[0].set_xlabel("Numer testu")
    ax[0].set_ylabel("Czas [us]")
    ax[0].legend()

    ax[1].set_ylim(ylim)

    for i in range(NODES_NO):
        df.plot(x='row_number', y=labels[i], color=colors[i], label=f"Węzeł {i}", kind='scatter', s=5, ax=ax[1])
    # ax[1].title("Przesunięcie zegarów")
    ax[1].set_xlabel("Numer testu")
    ax[1].set_ylabel("Czas [us]")
    ax[1].legend()
    ax[1].legend(loc='upper right')

    y_min, y_max = ylim
    ax[0].axhline(y=y_min, color='red', linestyle='--', xmin=ax[0].get_xlim()[0], xmax=ax[0].get_xlim()[1])
    ax[0].axhline(y=y_max, color='red', linestyle='--', xmin=ax[0].get_xlim()[0], xmax=ax[0].get_xlim()[1])

    con = ConnectionPatch(xyA=(ax[0].get_xlim()[1], y_min), xyB=(ax[1].get_xlim()[0], y_min), coordsA="data", coordsB="data", axesA=ax[0], axesB=ax[1], color="red", linestyle='--')
    fig.add_artist(con)
    con = ConnectionPatch(xyA=(ax[0].get_xlim()[1], y_max), xyB=(ax[1].get_xlim()[0], y_max), coordsA="data", coordsB="data", axesA=ax[0], axesB=ax[1], color="red", linestyle='--')
    fig.add_artist(con)

    fig.tight_layout()
    plt.savefig(f'../../charts/time_deltas/{name}.png', dpi=300)
    plt.close()

def plot_stddevs(df):
    stddevs = {x: df.std()[x] for x in labels}

    plt.bar(*zip(*stddevs.items()))
    plt.title("Odchylenia standardowe przesunięć")
    plt.xlabel("Numer węzła")
    plt.ylabel("Odchylenie [us]")
    plt.tight_layout()
    plt.savefig(f'../../charts/time_deltas/stddev.png', dpi=300)
    plt.close()

if __name__ == "__main__":

    df = pd.read_csv(f'time_deltas.csv')
    df = df.assign(row_number=range(len(df)))

    df[labels] -= df[labels].mean()

    plot_offsets(df, 'time_deltas', (-2000,2000))
    plot_stddevs(df)