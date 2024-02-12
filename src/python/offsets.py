import paho.mqtt.client as mqtt
import time
import csv

def calc_offset(client, consts, ctx):
    time_now = time.time_ns() // 1000
    client.publish(consts['topic'], str(time_now))
    for i in range(consts['no_nodes']):
        ctx['T1'][i] = time_now
    
    while None in ctx['T2p']:
        continue
    offsets = [None] * consts['no_nodes']
    for i in range(consts['no_nodes']):
        offsets[i] = (ctx['T1p'][i] -
                      ctx['T1'][i] +
                      ctx['T2p'][i] -
                      ctx['T2'][i]) / 2

    return offsets

def clear_ctx(ctx):
    ctx['T1'] = [None] * consts['no_nodes']
    ctx['T1p'] = [None] * consts['no_nodes']
    ctx['T2'] = [None] * consts['no_nodes']
    ctx['T2p'] = [None] * consts['no_nodes']

def on_connect(client, userdata, flags, rc):
    client.subscribe('source')
    for i in range(userdata['consts']['no_nodes']):
        client.subscribe(str(i))

def on_message(client, userdata, message):
    time_now = time.time_ns() // 1000
    node = int(message.topic)
    tokens = (message.payload).split()
    T1p = int(tokens[0])
    T2 = int(tokens[1])
    userdata['ctx']['T1p'][node] = T1p
    userdata['ctx']['T2'][node] = T2
    userdata['ctx']['T2p'][node] = time_now

def test(consts, ctx):
    client = mqtt.Client(userdata={'consts': consts, 'ctx': ctx})
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost",1883,60)
    client.loop_start()
    for i in range(1000):
        offsets = calc_offset(client, consts, ctx)
        ctx['offsets'].append(offsets)
        clear_ctx(ctx)
        time.sleep(0.1)
    client.loop_stop()
    
if __name__ == "__main__":
    consts = {'no_nodes': 4, 'topic': 'offset'}
    context = {'T1': [None] * consts['no_nodes'],
               'T1p': [None] * consts['no_nodes'],
               'T2': [None] * consts['no_nodes'],
               'T2p': [None] * consts['no_nodes'],
               'offsets': []}
    test(consts, context)
    with open('prop_time_sim.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['0', '1', '2', '3'])
        writer.writerows(context['offsets'])