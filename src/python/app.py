import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # for thermometer in temperatures.values():
    #     client.subscribe(thermometer['topic'])
    # for button in buttons.values():
    #     client.subscribe(button['topic'])
        
def on_message(client, userdata, message):
    print("Received message '" + str(float(message.payload)) + "' on topic '" + message.topic + "' with QoS " + str(message.qos))
    # for thermometer in temperatures.values():
    #     if message.topic == thermometer['topic']:
    #         print("temperature update")
    #         thermometer['temp'] = float(message.payload)
    #         socketio.emit('temperature', {'data': thermometer['temp']})
    #         tempHistory[0].append(float(message.payload))
    #         thermometer['history'] = list(tempHistory[0])
    #         socketio.emit('tempHistory', {'index': 0, 'array': list(thermometer['history'])})
    #         print(str(list(thermometer['history'])))
    #     for button in buttons.values():
    #         if message.topic == button['topic']:
    #             print("button update")
    #             button['presses'] += 1
    #             socketio.emit('button', button['presses'])

def publish_time(client):
    topic = 'chronos'
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f'sync_msg'
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        if msg_count > 5:
            break


def run():
    client = mqtt.Client()             
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost",1883,60)
    client.loop_start()
    publish_time(client)
    client.loop_stop()
    
# @app.route("/<board>/<changePin>/<action>")
# def action(board, changePin, action):
#     changePin = int(changePin)
#     if action == "1" and board == 'ESP01_RELAY':
#         client.publish(pins[changePin]['topic'],"1")
#         pins[changePin]['state'] = 'True'
#     if action == "0" and board == 'ESP01_RELAY':
#         client.publish(pins[changePin]['topic'],"0")
#         pins[changePin]['state'] = 'False'
    
#     templateData = {
#         'pins' : pins,
#         'temps' : temperatures,
#         'butts' : buttons
#     }
    
#     return render_template('main.html', **templateData)
    
if __name__ == "__main__":
    run()