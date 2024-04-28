import paho.mqtt.client as mqtt
import time
import csv

# def calc_deltas(client, consts, ctx):

def on_connect(client, userdata, flags, rc):
    client.subscribe('source')
    for i in range(userdata['consts']['nodes']):
        client.subscribe(str(i))

def on_message(client, userdata, message):
    time_now = time.time_ns() // 1000
    node = int(message.topic)
    tokens = (message.payload).split()
    message_no = int(tokens[0])
    send_time = int(tokens[1])
    # print(f"node: {node}, message: {message_no}, time: {time_now - send_time}")
    userdata['ctx']['receive_times'][node].append(time_now - send_time)
    
def get_times(client, consts, ctx):
    client.publish(consts['topic'], 'begin')
    while len(ctx['receive_times'][0]) < consts['messages']:
        continue

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
    consts = {'nodes': 4, 'messages': 4999, 'topic': 'synch'}
    context = {'receive_times': [[] for n in range(consts['nodes'])]}
    for i in range(10):
        test(consts, context)
        with open(f'data/message_times_{i}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([str(i) for i in range(consts['nodes'])])
            for i in range(consts['messages']):
                writer.writerow([context['receive_times'][node][i] for node in range(consts['nodes'])])
        context = {'receive_times': [[] for n in range(consts['nodes'])]}
