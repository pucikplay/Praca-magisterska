import matplotlib.pyplot as plt
import pandas as pd

def plot_dists(df, name, ylim):
    fig, ax = plt.subplots()
    if ylim is not None:
        ax.set_ylim(ylim)

    df_T = df.T.reset_index()
    df_T.drop(df_T.tail(1).index, inplace=True)
    df_T['index2'] = df_T['index']
    df_T = df_T.astype(float)

    df_T.plot(x='index', y='index2', ax=ax)
    for y in range(10):
        df_T.plot(x='index', y=y, color='red', kind='scatter', s=10, ax=ax)

    plt.title("Obliczone odległości")
    plt.xlabel("Rzeczywista odległość")
    plt.ylabel("Obliczona odległość")
    ax.get_legend().remove()
    plt.tight_layout()
    plt.savefig(f'../../charts/mic_sync_dist/{name}.png', dpi=300)
    plt.close()


if __name__ == '__main__':
    df = pd.read_csv('mic_sync_dist.csv')
    df = df.assign(row_number=range(len(df)))

    plot_dists(df, 'dists', None)
    plot_dists(df, 'dists_close', (-.1, 3.5))