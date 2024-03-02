import matplotlib.pyplot as plt
import pandas as pd

paths = ['prop_time_diff.csv', 'prop_time_sim.csv']
NODES_NO = 4
labels = ['0', '1', '2', '3']
colors = ['r', 'g', 'b', 'y']


def plot_points(df, name, ylim):
    fig, ax = plt.subplots()
    if ylim is not None:
        ax.set_ylim(ylim)

    for i in range(NODES_NO):
        df.plot(x='row_number', y=labels[i], color=colors[i], label=f"Node {i}", kind='scatter', s=5, ax=ax)
    plt.title("Transit time")
    plt.xlabel("Test no.")
    plt.ylabel("Time [us]")
    plt.legend()
    plt.savefig(f"{name}.png", dpi=300)

def plot_properties(df, name, ylim):
    for label in labels:
        df[f'{label}_mean'] = [df[label].mean()] * len(df)
        
    for label in labels:
        df[f'{label}_hmean'] = [len(df) / (1/df[label]).sum()] * len(df)

    fig, ax = plt.subplots()
    if ylim is not None:
        ax.set_ylim(ylim)
    # for i in range(NODES_NO):
    #     df.plot(x='row_number', y=f'{labels[i]}_mean', color=colors[i], label=f"Node {i}", ax=ax)

    for i in range(NODES_NO):
        df.plot(x='row_number', y=f'{labels[i]}_hmean', color=colors[i], label=f"Node {i}", ax=ax)

    # for i in range(NODES_NO):
    #     df.plot(x='row_number', y=labels[i], color=colors[i], label=f"Node {i}", kind='scatter', s=5, ax=ax)

    plt.title("Transit time")
    plt.xlabel("Test no.")
    plt.ylabel("Time [us]")
    plt.legend()
    plt.savefig(f"{name}_properties.png", dpi=300)

if __name__ == "__main__":
    df_diff = pd.read_csv(paths[0])
    df_diff = df_diff.assign(row_number=range(len(df_diff)))
    df_sim = pd.read_csv(paths[1])
    df_sim = df_sim.assign(row_number=range(len(df_sim)))

    plot_points(df_diff, "diff", None)
    plot_points(df_sim, "sim", (0, 70000))
    plot_properties(df_diff, "diff", None)
    plot_properties(df_sim, "sim", None)