import matplotlib.pyplot as plt
import numpy as np
import os
import re
import pandas as pd

def plot_charts(df, point, nodes, lims):
    fig, ax = plt.subplots()
    if lims is not None:
        ax.set_xlim(lims['xlim'])
        ax.set_ylim(lims['ylim'])

    df.plot(x='x', y='y', kind='scatter', s=10, ax=ax)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.title(f'Punkt {point}, pozycja odbiornika')
    fig.set_size_inches(8,6)
    fig.set_dpi(600)
    if lims is not None:
        fig.savefig(f'../../charts/mult_lat_2d/position_{point}_{nodes}_close.png')
    else:
        fig.savefig(f'../../charts/mult_lat_2d/position_{point}_{nodes}.png')
    plt.close()

def get_cmap(n, name='hsv'):
    return plt.cm.get_cmap(name, n)

def plot_multiple(df_dict, lims, num, mean=False):
    fig, ax = plt.subplots()
    if lims is not None:
        ax.set_xlim(lims['xlim'])
        ax.set_ylim(lims['ylim'])

    cmap = get_cmap(len(df_dict)+1)

    for i, (point, df) in enumerate(df_dict.items()):
        if mean:
            df_mean = pd.DataFrame(df.mean()).T
            df_mean.plot(x='x', y='y', kind='scatter', s=100, ax=ax, label=point, color=cmap(i))
        else:
            df.plot(x='x', y='y', kind='scatter', s=10, ax=ax, label=point, color=cmap(i))
        
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.title(f'Pozycje odbiornika')
    fig.set_size_inches(8,6)
    fig.set_dpi(600)
    if mean:
        fig.savefig(f'../../charts/mult_lat_2d/positions_{num}_mean.png')
    else:
        fig.savefig(f'../../charts/mult_lat_2d/positions_{num}.png')
    plt.close()

# 0: [0.3, 0.3]
# 1: [-0.3, 0.3]
# 2: [-0.3, -0.3]
# 3: [0.3, -0.3]

if __name__ == '__main__':
    df_dict = {}
    directory = os.fsencode('.')
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".csv"):
            df = pd.read_csv(filename)
            df = df[df > -1]
            df = df[df < 1]
            point = re.findall('\[.*\]',filename)[0]
            nodes = filename[filename.rfind('_')+1:-4]
            df_dict[point] = df
            # plot_charts(df, point, nodes, None)
            # plot_charts(df, point, nodes, lims[f'{point}_{nodes}'])

    # print(df_dict.keys())
    dict_1 = {point: df_dict[point] for point in ['[0, 0]',
                                                  '[0.3, 0.3]',
                                                  '[-0.3, 0.3]',
                                                  '[-0.3, -0.3]',
                                                  '[0.3, -0.3]']}

    dict_2 = {point: df_dict[point] for point in ['[0, 0]',
                                                  '[0, 0.3]',
                                                  '[0, -0.3]',
                                                  '[0.3, 0]',
                                                  '[-0.3, 0]']}
    
    dict_3 = {point: df_dict[point] for point in ['[0, 0]',
                                                  '[0.15, 0.15]',
                                                  '[-0.15, 0.15]',
                                                  '[-0.15, -0.15]',
                                                  '[0.15, -0.15]']}

    plot_multiple(dict_1, {'xlim': (-0.4, 0.9), 'ylim': (-0.8, 0.4)}, 1)
    plot_multiple(dict_2, {'xlim': (0, 0.5), 'ylim': (-0.6, 0.1)}, 2)
    plot_multiple(dict_3, {'xlim': (-0.8, 0.4), 'ylim': (-0.9, 0.3)}, 3)
    plot_multiple(dict_1, {'xlim': (-0.4, 0.9), 'ylim': (-0.8, 0.4)}, 1, mean=True)
    plot_multiple(dict_2, {'xlim': (0, 0.5), 'ylim': (-0.6, 0.1)}, 2, mean=True)
    plot_multiple(dict_3, {'xlim': (-0.8, 0.4), 'ylim': (-0.9, 0.3)}, 3, mean=True)