import matplotlib.pyplot as plt
import numpy as np
import os
import re
import pandas as pd

def plot_charts(df, point, nodes, ylim):
    df = df.reset_index()
    df['index_2'] = df['index'] / 2
    # print(point)
    # print(df)

    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax2 = ax1.twiny()
    if ylim is not None:
        ax1.set_ylim(ylim)
        ax2.set_ylim(ylim)

    df.plot(x='index', y='x', kind='scatter', s=10, ax=ax1)
    df.plot(x='index_2', y='x', kind='scatter', s=10, ax=ax2)
    ax1.set_xlabel('Numer kalkulacji pozycji')
    ax2.set_xlabel('Czas [s]')
    ax1.set_ylabel('Obliczona pozycja nadajnika [m]')
    plt.title(f'Punkt {point}, pozycja odbiornika')
    fig.set_size_inches(8,6)
    fig.set_dpi(600)
    if ylim is not None:
        fig.savefig(f'../../charts/mult_lat_1d/position_{point}_{nodes}_close.png')
    else:
        fig.savefig(f'../../charts/mult_lat_1d/position_{point}_{nodes}.png')
    plt.close()

# 0: [-0.5]
# 1: [0.5]
# 2: [0.2]
# 3: [-0.2]

if __name__ == '__main__':
    lims = {'[0]_4': (-0.04, 0.02),
            '[-0.5]_4': (-0.65, -0.4),
            '[0.5]_4': (0.45, 0.55),
            '[-0.25]_4': (-0.4, -0.2),
            '[0.25]_4': (0.1, 0.4),
            "[\'oscilate\']_4": None,
            '[0]_2': (0.0, 0.1),
            '[-0.5]_2': (-0.65, -0.5),
            '[0.5]_2': (0.5, 0.53),
            '[-0.25]_2': (-0.3, -0.1),
            '[0.25]_2': (0.28, 0.4),
            "[\'oscilate\']_2": None}
    directory = os.fsencode('.')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            df = pd.read_csv(filename)
            point = re.findall('\[.*\]',filename)[0]
            nodes = filename[filename.rfind('_')+1:-4]
            plot_charts(df, point, nodes, None)
            plot_charts(df, point, nodes, lims[f'{point}_{nodes}'])