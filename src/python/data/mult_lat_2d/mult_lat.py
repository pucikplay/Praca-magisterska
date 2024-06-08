import matplotlib.pyplot as plt
import numpy as np
import os
import re
import pandas as pd
import colorsys
import matplotlib.colors as mc

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

def lighten_color(color, amount=0.5):
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

def plot_multiple(df_dict, lims, num, mean=False):
    fig, ax = plt.subplots()
    if lims is not None:
        ax.set_xlim(lims['xlim'])
        ax.set_ylim(lims['ylim'])

    cmap = get_cmap(len(df_dict)+1)

    for i, (point, df) in enumerate(df_dict.items()):
        x, y = float(point[1:point.rfind(',')]), float(point[point.rfind(',')+1:-1])
        if mean:
            df_mean = pd.DataFrame(df.mean()).T
            df_mean.plot(x='x', y='y', kind='scatter', s=100, ax=ax, label=point, color=cmap(i))
            ax.scatter(x, y, color=lighten_color(cmap(i), 0.4))
        else:
            df.plot(x='x', y='y', kind='scatter', s=10, ax=ax, label=point, color=cmap(i))
        
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_aspect('equal', adjustable='box')
    # plt.title(f'Pozycje odbiornika')
    fig.set_size_inches(6,6)
    fig.set_dpi(600)
    fig.tight_layout()
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

    size = 0.85

    plot_multiple(dict_1, {'xlim': (-size, size), 'ylim': (-size, size)}, 1)
    plot_multiple(dict_2, {'xlim': (-size, size), 'ylim': (-size, size)}, 2)
    plot_multiple(dict_3, {'xlim': (-size, size), 'ylim': (-size, size)}, 3)
    plot_multiple(dict_1, {'xlim': (-size, size), 'ylim': (-size, size)}, 1, mean=True)
    plot_multiple(dict_2, {'xlim': (-size, size), 'ylim': (-size, size)}, 2, mean=True)
    plot_multiple(dict_3, {'xlim': (-size, size), 'ylim': (-size, size)}, 3, mean=True)