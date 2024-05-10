import paho.mqtt.client as mqtt
import time
import numpy as np
import pandas as pd
from scipy import stats
from math import trunc

def calc_offset(client, consts, ctx):
    time_now = time.time_ns() // 1000
    client.publish(consts['topic'], str(time_now))
    for i in range(consts['all_nodes']):
        ctx['T1'][i] = time_now
    
    while None in ctx['T2p']:
        continue
    offsets = [None] * consts['all_nodes']
    for i in range(consts['all_nodes']):
        offsets[i] = (ctx['T1p'][i] -
                      ctx['T1'][i] +
                      ctx['T2'][i] -
                      ctx['T2p'][i]) / 2

    return offsets

def clear_ctx(ctx):
    ctx['T1'] = [None] * consts['all_nodes']
    ctx['T1p'] = [None] * consts['all_nodes']
    ctx['T2'] = [None] * consts['all_nodes']
    ctx['T2p'] = [None] * consts['all_nodes']

def on_connect(client, userdata, flags, rc):
    client.subscribe('source')
    for i in range(userdata['consts']['nodes']):
        client.subscribe(str(i))

def on_message(client, userdata, message):
    if userdata['ctx']['sync']:
        time_now = time.time_ns() // 1000
        node = int(message.topic) if message.topic != 'source' else 1
        tokens = (message.payload).split()
        T1p = int(tokens[0])
        T2 = int(tokens[1])
        userdata['ctx']['T1p'][node] = T1p
        userdata['ctx']['T2'][node] = T2
        userdata['ctx']['T2p'][node] = time_now
    else:
        if message.topic == 'source':
            userdata['ctx']['last_src'] = int(message.payload)
            return
        node = int(message.topic)
        node_time = int(message.payload)
        # print(f"node: {node}, time: {node_time - userdata['ctx']['last_src']}")
        userdata['ctx']['node_times'][node].append(node_time -
                                                   userdata['ctx']['last_src'] +
                                                   userdata['ctx']['offsets'][-1])

def calc_offsets(client, consts, ctx):
    for i in range(200):
        print(i)
        offsets = calc_offset(client, consts, ctx)
        ctx['offsets'].append(offsets)
        clear_ctx(ctx)
        time.sleep(0.01)
    offsets = np.array(ctx['offsets'])
    print(offsets)
    offsets_df = pd.DataFrame.from_records(offsets, columns=consts['nodes_list'])
    offsets_df = offsets_df.drop([0])
    offsets_df.reset_index(drop=True, inplace=True)
    print(offsets_df)
    threshold_z = 2

    for node in range(consts['nodes']):
        z = np.abs(stats.zscore(offsets_df[node]))
        outlier_indices = np.where(z > threshold_z)[0]
        offsets_df.loc[outlier_indices, node] = 0

    offsets_df = offsets_df.replace(0, np.NaN)
    df_mean = offsets_df.mean()
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

def test_dist(client, consts, ctx):
    node = 0
    real_dists = consts['test_dists']
    calced_dists = {dist: [] for dist in real_dists}
    for dist in real_dists:
        input(f'Put node at {dist}[m]')
        client.publish(consts['src_topic'], '1')
        time.sleep(1.0)
        for _ in range(consts['messages']):
            dists = calc_dist(consts, ctx)
            # print(dists)
            calced_dists[dist].append(dists[0])
            time.sleep(0.5)
        client.publish(consts['src_topic'], '0')
    dist_df = pd.DataFrame.from_dict(calced_dists, orient='index').transpose()
    dist_df = dist_df.drop([0])
    dist_df.reset_index(drop=True, inplace=True)
    dist_df.to_csv('data/ntp_sync_dist_3.csv', index=False)

def test(consts, ctx):
    client = mqtt.Client(userdata={'consts': consts, 'ctx': ctx})
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost",1883,60)
    client.loop_start()
    calc_offsets(client, consts, ctx)
    ctx['sync'] = False
    client.publish('sync', '0')
    test_dist(client, consts, ctx)
    client.loop_stop()
    
if __name__ == "__main__":
    consts = {'nodes': 1,
              'all_nodes': 2,
              'nodes_list': [0, 'source'],
              'topic': 'offset',
              'src_topic': 'source',
              'messages': 11,
              'SS': 343,
              'test_dists': [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]}
    context = {'T1': [None] * consts['all_nodes'],
               'T1p': [None] * consts['all_nodes'],
               'T2': [None] * consts['all_nodes'],
               'T2p': [None] * consts['all_nodes'],
               'offsets': [],
               'sync': True,
               'node_times': [[] for n in range(consts['nodes'])],
               'last_src': 0}
    
    test(consts, context)