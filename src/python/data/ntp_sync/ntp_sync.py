import matplotlib.pyplot as plt
import pandas as pd

NODES_NO = 4
labels = ['0', '1', '2', '3']
colors = ['r', 'g', 'b', 'y']


def plot_offsets(df, name, ylim, normalize):
    fig, ax = plt.subplots()
    if ylim is not None:
        ax.set_ylim(ylim)

    if normalize:
        df[labels] -= df[labels].mean()

    for i in range(NODES_NO):
        df.plot(x='row_number', y=labels[i], color=colors[i], label=f"Węzeł {i}", kind='scatter', s=5, ax=ax)
    plt.title("Przesunięcie zegarów")
    plt.xlabel("Numer testu")
    plt.ylabel("Czas [us]")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'../../charts/ntp_sync/{name}.png', dpi=300)
    plt.close()

def plot_prop_times(df, name, ylim):
    fig, ax = plt.subplots()
    if ylim is not None:
        ax.set_ylim(ylim)

    for i in range(NODES_NO):
        df.plot(x='row_number', y=labels[i], color=colors[i], label=f"Węzeł {i}", kind='scatter', s=5, ax=ax)
    plt.title("Czas propagacji")
    plt.xlabel("Numer testu")
    plt.ylabel("Czas [us]")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f'../../charts/ntp_sync/{name}.png', dpi=300)
    plt.close()

def plot_stddevs(df_offsets, df_prop):
    stddevs_offsets = {x: df_offsets.std()[x] for x in labels}
    stddevs_props = {x: df_prop.std()[x] for x in labels}

    plt.bar(*zip(*stddevs_offsets.items()))
    plt.title("Odchylenia standardowe przesunięć")
    plt.xlabel("Numer węzła")
    plt.ylabel("Odchylenie [us]")
    plt.tight_layout()
    plt.savefig(f'../../charts/ntp_sync/stddev_offsets.png', dpi=300)
    plt.close()

    plt.bar(*zip(*stddevs_props.items()))
    plt.title("Odchylenia standardowe czasu propagacji")
    plt.xlabel("Numer węzła")
    plt.ylabel("Odchylenie [us]")
    plt.tight_layout()
    plt.savefig(f'../../charts/ntp_sync/stddev_prop.png', dpi=300)
    plt.close()

if __name__ == "__main__":
    df_offsets = pd.read_csv('clock_offsets.csv')
    df_offsets = df_offsets.assign(row_number=range(len(df_offsets)))
    df_prop = pd.read_csv('prop_times.csv')
    df_prop = df_prop.assign(row_number=range(len(df_prop)))

    plot_offsets(df_offsets, 'offsets', None, True)
    plot_prop_times(df_prop, 'prop_times', None)
    plot_offsets(df_offsets, 'offsets_close', (-5000,5000), True)
    plot_prop_times(df_prop, 'prop_times_close', (207500, 217500))
    plot_stddevs(df_offsets, df_prop)