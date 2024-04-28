import paho.mqtt.client as mqtt
import time
import csv

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
    for i in range(consts['nodes']):
        input(f"Node: {i}")
        client.publish(consts['sync_topic'], str(i))
        client.publish('src', '1')
        while len(ctx['node_times'][i]) < consts['messages']:
            continue
        client.publish(consts['sync_topic'], str(i))
        client.publish(consts['src_topic'], '0')

def test(consts, ctx):
    client = mqtt.Client(userdata={'consts': consts, 'ctx': ctx})
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost",1883,60)
    client.loop_start()
    # initialize communication
    get_times(client, consts, ctx)
    client.loop_stop()
    
if __name__ == "__main__":
    consts = {'nodes': 4, 'messages': 10, 'sync_topic': 'sync', 'src_topic': 'src'}
    context = {'node_times': [[] for n in range(consts['nodes'])],
                'last_src': 0}
    for i in range(6):
        test(consts, context)
        print(context)
        with open(f'data/node_times_{i}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(i) for i in range(consts['nodes'])])
            for i in range(consts['messages']):
                writer.writerow([context['node_times'][node][i] for node in range(consts['nodes'])])
        context = {'node_times': [[] for n in range(consts['nodes'])],
                   'last_src': 0}
