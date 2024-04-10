import matplotlib.pyplot as plt
import pandas as pd
from math import sqrt

NODES_NO = 4
FILES_NO = 6
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
        df_std = df.std()
        df_mean = df.mean()
        for col in df:
            for value in df[col].values:
                if abs(value - df_mean[col]) > 2 * df_std[col]:
                    print(value)
                    df.replace(value,df_mean[col],inplace=True)
        data.append(df)

    plot_individual(data)
    plot_means(data)