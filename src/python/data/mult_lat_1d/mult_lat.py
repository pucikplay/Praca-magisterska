import matplotlib.pyplot as plt
import numpy as np
import os
import re
import pandas as pd
import colorsys
import matplotlib.colors as mc

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

def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)

def lighten_color(color, amount=0.5):
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

def plot_multiple(df_dict, lims, nodes, mean=False):
    fig, ax = plt.subplots()
    if lims is not None:
        ax.set_xlim(lims['xlim'])
        ax.set_ylim(lims['ylim'])

    cmap = get_cmap(len(df_dict)+1)

    for i, (point, df) in enumerate(df_dict.items()):
        x, y = float(point[1:-1]), 0
        if mean:
            df_mean = pd.DataFrame(df.mean()).T
            df_mean['y'] = 0
            df_mean.plot(x='x', y='y', kind='scatter', s=100, ax=ax, label=point, color=cmap(i))
            ax.scatter(x, y, color=lighten_color(cmap(i), 0.4))
        else:
            df['y'] = 0
            df.plot(x='x', y='y', kind='scatter', s=10, ax=ax, label=point, color=cmap(i))
    
    ax.legend(loc="upper left", ncol=(len(df_dict)+1)//2)
    ax.set_xlabel('x')
    ax.set_ylabel('')
    ax.set_yticklabels([])
    ax.set_yticks([])
    # plt.title(f'Pozycje odbiornika')
    fig.set_size_inches(6,3)
    fig.set_dpi(600)
    fig.tight_layout()
    if mean:
        fig.savefig(f'../../charts/mult_lat_1d/positions_{nodes}_mean.png')
    else:
        fig.savefig(f'../../charts/mult_lat_1d/positions_{nodes}.png')
    plt.close()

# 0: [-0.5]
# 1: [0.5]
# 2: [0.2]
# 3: [-0.2]

# if __name__ == '__main__':
#     lims = {'[0]_4': (-0.04, 0.02),
#             '[-0.5]_4': (-0.65, -0.4),
#             '[0.5]_4': (0.45, 0.55),
#             '[-0.25]_4': (-0.4, -0.2),
#             '[0.25]_4': (0.1, 0.4),
#             "[\'oscilate\']_4": None,
#             '[0]_2': (0.0, 0.1),
#             '[-0.5]_2': (-0.65, -0.5),
#             '[0.5]_2': (0.5, 0.53),
#             '[-0.25]_2': (-0.3, -0.1),
#             '[0.25]_2': (0.28, 0.4),
#             "[\'oscilate\']_2": None}
#     directory = os.fsencode('.')
#     for file in os.listdir(directory):
#         filename = os.fsdecode(file)
#         if filename.endswith(".csv"):
#             df = pd.read_csv(filename)
#             point = re.findall('\[.*\]',filename)[0]
#             nodes = filename[filename.rfind('_')+1:-4]
#             plot_charts(df, point, nodes, None)
#             plot_charts(df, point, nodes, lims[f'{point}_{nodes}'])

if __name__ == '__main__':
    nodes_num = ['2', '4']
    df_dict = {num: {} for num in nodes_num}
    directory = os.fsencode('.')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            df = pd.read_csv(filename)
            df = df[df > -2]
            df = df[df < 2]
            point = re.findall('\[.*\]', filename)[0] 
            nodes = filename[filename.rfind('_')+1:-4]
            df_dict[nodes][point] = df

    for num in nodes_num:
        plot_multiple(df_dict[num], {'xlim': (-0.7, 0.7), 'ylim': (-0.2, 0.2)}, num)
        plot_multiple(df_dict[num], {'xlim': (-0.7, 0.7), 'ylim': (-0.2, 0.2)}, num, mean=True)