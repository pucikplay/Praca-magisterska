import matplotlib.pyplot as plt
import pandas as pd

NODES_NO = 4
labels = ['0', '1', '2', '3']
colors = ['r', 'g', 'b', 'y']


def plot_offsets(df, name, ylim):
    fig, ax = plt.subplots()
    if ylim is not None:
        ax.set_ylim(ylim)
    
    ax.ticklabel_format(style='plain')

    for i in range(NODES_NO):
        df.plot(x='row_number', y=labels[i], color=colors[i], label=f"Węzeł {i}", kind='scatter', s=5, ax=ax)
    plt.title("Przesunięcie zegarów")
    plt.xlabel("Numer testu")
    plt.ylabel("Czas [us]")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'../../charts/mic_sync/{name}.png', dpi=300)

def plot_stddevs(df):
    stddevs = {x: df.std()[x] for x in labels}

    plt.bar(*zip(*stddevs.items()))
    plt.title("Odchylenia standardowe przesunięć")
    plt.xlabel("Numer węzła")
    plt.ylabel("Odchylenie [us]")
    plt.tight_layout()
    plt.savefig(f'../../charts/mic_sync/stddev_offsets.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    df = pd.read_csv('mic_sync.csv')
    df = df.assign(row_number=range(len(df)))

    df[labels] -= df['0'][0]

    plot_offsets(df, 'offsets', None)
    # plot_offsets(df_offsets, 'offsets_close', (-30000,-10000), True)
    plot_stddevs(df)