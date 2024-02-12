import paho.mqtt.client as mqtt
import time
from datetime import datetime
import numpy as np

SS = 343
NODES = 4
DIMS = 1
src_time = 0
node_times = [0] * NODES
coords = np.array([[-0.5],
                   [-0.5],
                   [0.5],
                   [0.5]])

def calcA(coords):
    A = np.zeros((NODES, DIMS + 1))
    A[:,0] = np.ones(NODES)
    for i in range(NODES):
        for j in range(DIMS):
            A[i][j+1] = -2 * coords[i][j]
    return A

A = calcA(coords)
AT = A.transpose()

M = np.matmul(np.linalg.inv(np.matmul(AT, A)), AT)

def calc_position():
    b = np.zeros(NODES)
    for i in range(NODES):
        s = (SS / 1000000) * (node_times[i] - src_time)
        b[i] = s - sum(coords[i]**2)
    return M.dot(b)[1]

def on_connect(client, userdata, flags, rc):
    # print("Connected with result code " + str(rc))
    client.subscribe('source')
    for i in range(NODES):
        client.subscribe(str(i))

def on_message(client, userdata, message):
    global src_time
    # print("Received message '" + str(int(message.payload)) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
    if message.topic == 'source':
        src_time = int(message.payload)
    else:
        node_times[int(message.topic)] = int(message.payload)

def run():
    client = mqtt.Client()             
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost",1883,60)
    client.loop_start()
    while(True):
        time.sleep(0.25)
        print(f'src_time: {src_time}')
        for node_time in node_times:
            print(node_time)
        print(calc_position())

if __name__ == "__main__":
    run()
