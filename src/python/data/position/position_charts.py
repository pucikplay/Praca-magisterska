import matplotlib.pyplot as plt
import numpy as np

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
        ax2 = ax1.twiny()

        ax1.scatter(x, y, s=3)
        ax2.scatter([d/2 for d in x], y, s=10)
        ax1.set_xlabel('Numer kalkulacji pozycji')
        ax2.set_xlabel('Czas [s]')
        ax1.set_ylabel('Obliczona pozycja nadajnika [m]')
        # fig.suptitle(f'Test {i}, pozycja')
        plt.title(f'Test {i}, pozycja odbiornika')
        fig.set_size_inches(8,6)
        fig.set_dpi(600)
        fig.savefig(f'position_{i}.png')

if __name__ == '__main__':
    plot_charts(5)