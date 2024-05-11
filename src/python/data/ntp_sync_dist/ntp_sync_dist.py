import matplotlib.pyplot as plt
import pandas as pd

def plot_dists(df, name, ylim, slope):
    fig, ax = plt.subplots()
    if ylim is not None:
        ax.set_ylim(ylim)

    df_T = df.T.reset_index()
    df_T.drop(df_T.tail(1).index, inplace=True)
    df_T['index2'] = df_T['index']
    df_T = df_T.astype(float)

    df_T.plot(x='index', y='index2', ax=ax, label='y=x')
    if slope is not None:
        df_T['index3'] = df_T['index'] * slope
        df_T = df_T.astype(float)
        df_T.plot(x='index', y='index3', ax=ax, label=f'y={slope}x')
    for y in range(10):
        df_T.plot(x='index', y=y, color='red', kind='scatter', s=10, ax=ax)

    plt.title("Obliczone odległości")
    plt.xlabel("Rzeczywista odległość")
    plt.ylabel("Obliczona odległość")
    ax.get_legend().remove()
    plt.tight_layout()
    plt.legend()
    plt.savefig(f'../../charts/ntp_sync_dist/{name}.png', dpi=300)
    plt.close()

if __name__ == '__main__':
    offsets = [23.35, 22.9, 23.5, 24.5]
    for i in range(4):
        df = pd.read_csv(f'ntp_sync_dist_{i}.csv')
        df = df.assign(row_number=range(len(df)))

        plot_dists(df, f'dists_{i}', None, None)
        df -= offsets[i]
        plot_dists(df, f'dists_close_{i}', (-.1, 3.5), 3)