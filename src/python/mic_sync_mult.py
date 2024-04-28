import paho.mqtt.client as mqtt
import time
import csv
from scipy import stats
import numpy as np
import pandas as pd
from math import trunc

def on_connect(client, userdata, flags, rc):
    client.subscribe('source')
    for i in range(userdata['consts']['nodes']):
        client.subscribe(str(i))

def on_message(client, userdata, message):
    if message.topic == 'source':
        userdata['ctx']['last_src'] = int(message.payload)
        return
    node = int(message.topic)
    node_time = int(message.payload)
    # print(f"node: {node}, time: {node_time - userdata['ctx']['last_src']}")
    userdata['ctx']['node_times'][node].append(node_time -
                                               userdata['ctx']['last_src'])
    
def get_times(client, consts, ctx):
    ctx['node_times'] = [[] for n in range(consts['nodes'])]
    for i in range(consts['nodes']):
        input(f"Node: {i}")
        client.publish(consts['sync_topic'], str(i))
        client.publish('src', '1')
        while len(ctx['node_times'][i]) < consts['messages']:
            continue
        client.publish(consts['sync_topic'], str(i))
        client.publish(consts['src_topic'], '0')
    node_times_df = pd.DataFrame.form_records(ctx['node_times'], columns=range(consts['nodes']))
    ctx['node_times_df'] = node_times_df

def calc_offsets(consts, ctx):
    node_times_df = ctx['node_times_df']
    # drop first values, most of the time erroneous
    node_times_df = df.drop([0])
    node_times_df.reset_index(drop=True, inplace=True)
    threshold_z = 2
    for node in range(NODES_NO):
        z = np.abs(stats.zscore(node_times_df[str(node)]))
        outlier_indices = np.where(z > threshold_z)[0]
        node_times_df.loc[outlier_indices, str(node)] = 0
    node_times_df = node_times_df.replace(0, np.NaN)
    df_mean = node_times_df.mean()
    ctx['offsets'] = [trunc(x) for x in list(df_mean)]
    # print(ctx['offsets'])

def calc_M(consts, ctx):
    nodes = consts['nodes']
    dims = consts['dims']
    coors = ctx['coords']
    A = np.zeros((nodes, dims + 1))
    A[:,0] = np.ones(nodes)
    for i in range(nodes):
        for j in range(dims):
            A[i][j+1] = -2 * coords[i][j]
    AT = A.transpose()
    M = np.matmul(np.linalg.inv(np.matmul(AT, A)), AT)
    ctx['M'] = M

def calc_position(consts, ctx):
    nodes = consts['nodes']
    M = ctx['M']
    SS = consts['SS']
    coors = ctx['coords']
    node_times = ctx['node_times']
    b = np.zeros(nodes)
    for node in range(nodes):
        s = (SS / 1000000) * (node_times[node][-1] - ctx['last_src'])
        b[node] = s - sum(coords[node]**2)
    return M.dot(b)#[1]

def run(consts, ctx):
    get_times(client, consts, ctx)
    calc_offsets(consts, ctx)
    
    # client.loop_stop()
    
if __name__ == "__main__":
    consts = {'nodes': 2,
              'dims': 1,
              'SS': 343,
              'messages': 10,
              'sync_topic': 'sync',
              'src_topic': 'src'}

    context = {'node_times': [[] for n in range(consts['nodes'])],
               'offsets': None,
               'coords': [-0.5, 0.5],
               'M': None,
               'last_src': 0}

    client = mqtt.Client(userdata={'consts': consts, 'ctx': context})
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost",1883,60)
    client.loop_start()
    run(consts, context)
