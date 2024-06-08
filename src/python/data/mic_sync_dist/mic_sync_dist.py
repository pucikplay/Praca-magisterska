import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import statsmodels.api as sm
from matplotlib.patches import ConnectionPatch

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

    # plt.title("Obliczone odległości")
    plt.xlabel("Rzeczywista odległość")
    plt.ylabel("Obliczona odległość")
    ax.get_legend().remove()
    plt.tight_layout()
    plt.legend()
    plt.savefig(f'../../charts/mic_sync_dist/{name}.png', dpi=300)
    plt.close()

def plot_dists_cmp(df, name, ylim, slope):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))

    df_T = df.T.reset_index()
    df_T.drop(df_T.tail(1).index, inplace=True)
    df_T['index2'] = df_T['index']
    df_T = df_T.astype(float)

    df_T.plot(x='index', y='index2', ax=ax[0], label='y=x')
    for y in range(df_T.shape[1]-3):
        df_T.plot(x='index', y=y, color='red', kind='scatter', s=10, ax=ax[0])

    # plt.title("Obliczone odległości")
    ax[0].set_xlabel("Rzeczywista odległość")
    ax[0].set_ylabel("Obliczona odległość")
    ax[0].get_legend().remove()
    ax[0].legend()

    ax[1].set_ylim(ylim)

    df_T.plot(x='index', y='index2', ax=ax[1], label='y=x')
    if slope is not None:
        df_T['index3'] = df_T['index'] * slope
        df_T = df_T.astype(float)
        df_T.plot(x='index', y='index3', ax=ax[1], label=f'y={slope}x')
    for y in range(df_T.shape[1]-3):
        df_T.plot(x='index', y=y, color='red', kind='scatter', s=10, ax=ax[1])

    # plt.title("Obliczone odległości")
    ax[1].set_xlabel("Rzeczywista odległość")
    ax[1].set_ylabel("Obliczona odległość")
    ax[1].get_legend().remove()
    ax[1].legend()

    y_min, y_max = ylim
    ax[0].axhline(y=y_min, color='green', linestyle='--', xmin=ax[0].get_xlim()[0], xmax=ax[0].get_xlim()[1])
    ax[0].axhline(y=y_max, color='green', linestyle='--', xmin=ax[0].get_xlim()[0], xmax=ax[0].get_xlim()[1])

    con = ConnectionPatch(xyA=(ax[0].get_xlim()[1], y_min), xyB=(ax[1].get_xlim()[0], y_min), coordsA="data", coordsB="data", axesA=ax[0], axesB=ax[1], color="green", linestyle='--')
    fig.add_artist(con)
    con = ConnectionPatch(xyA=(ax[0].get_xlim()[1], y_max), xyB=(ax[1].get_xlim()[0], y_max), coordsA="data", coordsB="data", axesA=ax[0], axesB=ax[1], color="green", linestyle='--')
    fig.add_artist(con)

    fig.tight_layout()
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

        plot_dists_cmp(df, f'dists_{i}', (-.1, 3.5), 3)
        plot_dists(df, f'dists_sep_{i}', None, None)
        plot_dists(df, f'dists_close_{i}', (-.1, 3.5), 3)

        df = pd.read_csv(f'mic_sync_dist_long_{i}.csv')

        plot_dists_cmp(df, f'dists_long_{i}', (-.1, 6.5), None)

        df = clean(df)
        data = pd.DataFrame(df)

        X = list(map(float, data.index.to_list()))
        Y = data[0].values
        model = sm.OLS(Y,X)
        result = model.fit()
        slope = round(result.params[0], 3)

        plot_dists(df, f'dists_close_long_{i}_mean', (-.1, 6.5), slope)