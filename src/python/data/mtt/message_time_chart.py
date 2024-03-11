import matplotlib.pyplot as plt
import pandas as pd

NODES_NO = 4
FILES_NO = 6
labels = [str(i) for i in range(NODES_NO)]
colors = ['r', 'g', 'b', 'y']


def plot_data(df, no):
    fig, ax = plt.subplots()

    for i in range(NODES_NO):
        df.plot(x='row_number', y=labels[i], color=colors[:NODES_NO][i], label=f"Node {i}", kind='scatter', s=5, ax=ax)
    
    plt.title("Message transit time")
    plt.xlabel("Message no.")
    plt.ylabel("Time [us]")
    plt.legend()
    plt.savefig(f"../../charts/mtt/mtt_{no}.png", dpi=300)

    df.hist(column=labels, bins=range(0,5000,300))
    
    plt.title("Message transit time")
    plt.xlabel("Message no.")
    plt.ylabel("Time [us]")
    plt.legend()
    plt.savefig(f"../../charts/mtt/mtt_bar_{no}.png", dpi=300)

    fig, ax = plt.subplots()

    for i in range(1,NODES_NO):
        df.plot(x='row_number', y=f'{labels[i]}_delta', color=colors[i], label=f"Node {i}", ax=ax)

    plt.title("Message transit time deltas")
    plt.xlabel("Message no.")
    plt.ylabel("Time [us]")
    plt.legend()
    plt.savefig(f"../../charts/mtt/mtt_delta_{no}.png", dpi=300)
    
def plot_deltas(df):
    df.plot.bar()
    plt.title("Message transit time deltas means")
    plt.xlabel("Test no.")
    plt.ylabel("Time [us]")
    plt.legend()
    plt.savefig(f"../../charts/mtt/mtt_deltas_means.png", dpi=300)

if __name__ == "__main__":

    means = []

    for i in range(FILES_NO):
        df = pd.read_csv(f'message_times_{i}.csv')
        df = df.assign(row_number=range(len(df)))

        df[labels] = df[labels] - df[labels].min() + 1 # avoid 0 in harmonic mean

        for label in labels[1:]:
            # df[f'{label}_mean'] = [df[label].mean()] * len(df)
            # df[f'{label}_hmean'] = [len(df) / (1/df[label]).sum()] * len(df)
            df[f'{label}_delta'] = df['0'] - df[label]

        means.append(df[[label + '_delta' for label in labels[1:]]].mean().tolist())
        plot_data(df, i)

    df_means = pd.DataFrame(means)
    # plot_deltas(df_means)