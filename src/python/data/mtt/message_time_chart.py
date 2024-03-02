import matplotlib.pyplot as plt
import pandas as pd

NODES_NO = 4
labels = ['0', '1', '2', '3']
colors = ['r', 'g', 'b', 'y']


def plot_points(df, ylim):
    fig, ax = plt.subplots()
    if ylim is not None:
        ax.set_ylim(ylim)

    for i in range(NODES_NO):
        df.plot(x='row_number', y=labels[i], color=colors[i], label=f"Node {i}", kind='scatter', s=5, ax=ax)
    plt.title("Message transit time")
    plt.xlabel("Message no.")
    plt.ylabel("Time [us]")
    plt.legend()
    plt.savefig(f"../../charts/mtt/mtt_5.png", dpi=300)
    

if __name__ == "__main__":
    df = pd.read_csv('message_times_5.csv')
    df = df.assign(row_number=range(len(df)))

    df[labels] = df[labels] - df[labels].min()
    # for i in range(1,NODES_NO):
    #     df[str(i)] = df[str(i)] - df['0']

    plot_points(df, None)