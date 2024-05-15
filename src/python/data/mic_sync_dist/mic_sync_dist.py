import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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
    for y in range(df_T.shape[1]-3):
        df_T.plot(x='index', y=y, color='red', kind='scatter', s=10, ax=ax)

    plt.title("Obliczone odległości")
    plt.xlabel("Rzeczywista odległość")
    plt.ylabel("Obliczona odległość")
    ax.get_legend().remove()
    plt.tight_layout()
    plt.legend()
    plt.savefig(f'../../charts/mic_sync_dist/{name}.png', dpi=300)
    plt.close()

def clean(df):
    outliers = df > 10.0
    df[outliers] = float('nan')
    df_mean = df.mean()
    return df_mean

if __name__ == '__main__':

    for i in range(4):
        df = pd.read_csv(f'mic_sync_dist_{i}.csv')
        df = df.assign(row_number=range(len(df)))

        plot_dists(df, f'dists_{i}', None, None)
        plot_dists(df, f'dists_close_{i}', (-.1, 3.5), 3)

        if i < 3:
            df = pd.read_csv(f'mic_sync_dist_long_{i}.csv')
            df = df.assign(row_number=range(len(df)))

            plot_dists(df, f'dists_long_{i}', None, None)
            plot_dists(df, f'dists_close_long_{i}', (-.1, 6.5), 2.5)

            df = clean(df)

            plot_dists(df, f'dists_close_long_{i}_mean', (-.1, 6.5), 2.5)