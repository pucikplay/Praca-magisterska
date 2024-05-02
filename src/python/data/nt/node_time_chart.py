import matplotlib.pyplot as plt
import pandas as pd
from math import sqrt,trunc
import numpy as np
from scipy import stats

NODES_NO = 4
FILES_NO = 1#6
labels = [str(i) for i in range(NODES_NO)]

def get_idx(i):
    a = i // 2
    b = i % 2
    return a,b

def plot_individual(data):
    fig, axs = plt.subplots(2,2)
    fig.tight_layout(pad=3)

    for df in data:
        for i in range(NODES_NO):
            axs[get_idx(i)].title.set_text(f"Node {i}")
            df[labels[i]].plot(style='.', ax=axs[get_idx(i)])
    fig.suptitle("Node offset individual")
    fig.supxlabel("Message no.")
    fig.supylabel("Time [us]")
    plt.savefig("../../charts/nt/nt.png", dpi=300)

def plot_means(data):
    fig, axs = plt.subplots(2,2)
    fig.tight_layout(pad=3)

    for df in data:    
        df_mean = df.mean()
        
    fig.suptitle("Node offset means")
    fig.supxlabel("Test no.")
    fig.supylabel("Time [us]")
    plt.savefig("../../charts/nt/nt_means.png", dpi=300)

if __name__ == "__main__":

    data = []

    for file in range(FILES_NO):
        df = pd.read_csv(f'node_times_{file}.csv')
        df = df.drop([0])
        df.reset_index(drop=True, inplace=True)
        df_std = df.std()
        # df_mean = df.mean()
        threshold_z = 2
        print(df)
        print(df.mean())
        for node in range(NODES_NO):
            z = np.abs(stats.zscore(df[str(node)]))
            outlier_indices = np.where(z > threshold_z)[0]
            df.loc[outlier_indices, str(node)] = 0
        df = df.replace(0, np.NaN)
        print([trunc(x) for x in list(df.mean())])
        # for col in df:
        #     for value in df[col].values:
        #         if abs(value - df_mean[col]) > 2 * df_std[col]:
        #             print(value)
        #             df.replace(value,df_mean[col],inplace=True)
        # data.append(df)

    # plot_individual(data)
    # plot_means(data)