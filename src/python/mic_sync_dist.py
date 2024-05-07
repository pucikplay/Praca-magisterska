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
    for node in range(consts['nodes']):
        input(f"Testing node {node}")
        client.publish(consts['sync_topic'], str(node))
        client.publish(consts['src_topic'], '1')
        while len(ctx['node_times'][node]) < consts['messages']:
            continue
        client.publish(consts['sync_topic'], str(node))
        client.publish(consts['src_topic'], '0')

    data = []
    arr = np.array(ctx['node_times'])
    for i in range(consts['messages']):
        data.append(arr[:,i])
    node_times_df = pd.DataFrame.from_records(data, columns=range(consts['nodes']))
    ctx['node_times_df'] = node_times_df

def calc_offsets(consts, ctx):
    node_times_df = ctx['node_times_df']
    # drop first values, most of the time erroneous
    node_times_df = node_times_df.drop([0])
    node_times_df.reset_index(drop=True, inplace=True)
    threshold_z = 2

    for node in range(consts['nodes']):
        z = np.abs(stats.zscore(node_times_df[node]))
        outlier_indices = np.where(z > threshold_z)[0]
        node_times_df.loc[outlier_indices, node] = 0

    node_times_df = node_times_df.replace(0, np.NaN)
    df_mean = node_times_df.mean()
    ctx['offsets'] = [trunc(x) for x in list(df_mean)]
    print(f'Node clock offsets: {ctx["offsets"]}')

def calc_dist(consts, ctx):
    nodes = consts['nodes']
    SS = consts['SS']
    node_times = ctx['node_times']
    dists = np.zeros(nodes)
    for node in range(nodes):
        delta_t = node_times[node][-1] - ctx['offsets'][node]
        d = (SS / 1000000) * delta_t
        dists[node] = d
    return dists

def test_dist(consts, ctx):
    node = 0
    real_dists = consts['test_dists']
    calced_dists = {dist: [] for dist in real_dists}
    for dist in real_dists:
        input(f'Put node at {dist}[m]')
        client.publish(consts['sync_topic'], str(node))
        client.publish(consts['src_topic'], '1')
        for _ in range(consts['messages']):
            dists = calc_dist(consts, ctx)
            calced_dists[dist].append(dists[0])
            time.sleep(0.5)
        client.publish(consts['sync_topic'], str(node))
        client.publish(consts['src_topic'], '0')
    dist_df = pd.DataFrame.from_dict(calced_dists, orient='index').transpose()
    dist_df = dist_df.drop([0])
    dist_df.reset_index(drop=True, inplace=True)
    dist_df.to_csv('data/mic_sync_dist.csv', index=False)

def run(consts, ctx):
    get_times(client, consts, ctx)
    calc_offsets(consts, ctx)
    input('Begin test')
    test_dist(consts, ctx)

if __name__ == "__main__":
    consts = {'nodes': 1,
              'dims': 1,
              'SS': 343,
              'messages': 11,
              'test_dists': [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0],
              'sync_topic': 'active',
              'src_topic': 'src'}

    context = {'node_times': [[] for n in range(consts['nodes'])],
               'offsets': None,
               'last_src': 0}

    client = mqtt.Client(userdata={'consts': consts, 'ctx': context})
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost",1883,60)
    client.loop_start()
    run(consts, context)
    client.loop_stop()
