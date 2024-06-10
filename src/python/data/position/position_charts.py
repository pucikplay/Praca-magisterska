import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import ConnectionPatch

def plot_charts_cmp(n,m):
    ylims = [(-0.76,-0.44),(72.2,72.65),(74.45,74.64)]
    ylims2 = [(-13.4,-12.85),(-11.5,-11.3)]
    fontsize = 12
    for i in range(n,m):
        positions = []
        with open(f'position_{i}.csv') as f:
            for line in f:
                pos = float(line)
                positions.append(pos)
            f.close()
    
        x = [d for d in range(len(positions))]
        y = positions
        ylim = ylims[i-2]

        fig = plt.figure(figsize=(12,6))
        gs = fig.add_gridspec(2,3)
        ax = [None, None, None]
        ax[0] = fig.add_subplot(gs[:, 0])
        if i == 2:
            ax[1] = fig.add_subplot(gs[:, 1:])
        else:
            ax[1] = fig.add_subplot(gs[0, 1:])
            ax[2] = fig.add_subplot(gs[1, 1:])
        
        ax[0].scatter(x, y, s=10)
        ax[0].set_xlabel('Numer kalkulacji pozycji', size=fontsize)
        ax[0].set_ylabel('Obliczona pozycja nadajnika [m]', size=fontsize)
        ax[0].tick_params(axis='x', labelsize=fontsize)
        ax[0].tick_params(axis='y', labelsize=fontsize)

        if i == 2:
            ax[1].set_ylim(ylim)

            ax[1].scatter(x, y, s=10)
            ax[1].set_xlabel('')
            ax[1].set_ylabel('')
            ax[1].tick_params(axis='x', labelsize=fontsize)
            ax[1].tick_params(axis='y', labelsize=fontsize)

        if i != 2:
            ylim2 = ylims2[i-3]

            ax[1].set_ylim(ylim)

            ax[1].scatter(x, y, s=10)
            ax[1].set_xlabel('')
            ax[1].set_ylabel('')
            ax[1].tick_params(axis='x', labelsize=fontsize)
            ax[1].tick_params(axis='y', labelsize=fontsize)

            ax[2].set_ylim(ylim2)

            ax[2].scatter(x, y, s=10)
            ax[2].set_xlabel('')
            ax[2].set_ylabel('')
            ax[2].tick_params(axis='x', labelsize=fontsize)
            ax[2].tick_params(axis='y', labelsize=fontsize)
        
        y_min, y_max = ylim
        ax[0].axhline(y=y_min, color='red', linestyle='--', xmin=ax[0].get_xlim()[0], xmax=ax[0].get_xlim()[1])
        ax[0].axhline(y=y_max, color='red', linestyle='--', xmin=ax[0].get_xlim()[0], xmax=ax[0].get_xlim()[1])

        con = ConnectionPatch(xyA=(ax[0].get_xlim()[1], y_min), xyB=(ax[1].get_xlim()[0], y_min), coordsA="data", coordsB="data", axesA=ax[0], axesB=ax[1], color="red", linestyle='--')
        fig.add_artist(con)
        con = ConnectionPatch(xyA=(ax[0].get_xlim()[1], y_max), xyB=(ax[1].get_xlim()[0], y_max), coordsA="data", coordsB="data", axesA=ax[0], axesB=ax[1], color="red", linestyle='--')
        fig.add_artist(con)

        if i != 2:
            y_min, y_max = ylim2
            ax[0].axhline(y=y_min, color='red', linestyle='--', xmin=ax[0].get_xlim()[0], xmax=ax[0].get_xlim()[1])
            ax[0].axhline(y=y_max, color='red', linestyle='--', xmin=ax[0].get_xlim()[0], xmax=ax[0].get_xlim()[1])

            con = ConnectionPatch(xyA=(ax[0].get_xlim()[1], y_min), xyB=(ax[2].get_xlim()[0], y_min), coordsA="data", coordsB="data", axesA=ax[0], axesB=ax[2], color="red", linestyle='--')
            fig.add_artist(con)
            con = ConnectionPatch(xyA=(ax[0].get_xlim()[1], y_max), xyB=(ax[2].get_xlim()[0], y_max), coordsA="data", coordsB="data", axesA=ax[0], axesB=ax[2], color="red", linestyle='--')
            fig.add_artist(con)

        fig.set_dpi(600)
        fig.tight_layout()
        fig.savefig(f'../../charts/position/position_{i}.png')
        plt.close()

def plot_charts(n):
    for i in range(n):
        positions = []
        with open(f'position_{i}.csv') as f:
            for line in f:
                pos = float(line)
                positions.append(pos)
            f.close()
    
        x = [d for d in range(len(positions))]
        y = positions

        fig = plt.figure()
        ax1 = fig.add_subplot()
        # ax2 = ax1.twiny()

        ax1.scatter(x, y, s=10)
        # ax2.scatter([d/2 for d in x], y, s=10)
        ax1.set_xlabel('Numer kalkulacji pozycji')
        # ax2.set_xlabel('Czas [s]')
        ax1.set_ylabel('Obliczona pozycja nadajnika [m]')
        # fig.suptitle(f'Test {i}, pozycja')
        # plt.title(f'Test {i}, pozycja odbiornika')
        fig.set_size_inches(10,4)
        fig.set_dpi(600)
        fig.tight_layout()
        fig.savefig(f'../../charts/position/position_{i}.png')

if __name__ == '__main__':
    plot_charts(5)
    plot_charts_cmp(2,5)