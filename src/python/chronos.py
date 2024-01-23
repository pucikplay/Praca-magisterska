import paho.mqtt.client as mqtt
import time

def publish_time(client):
    topic = 'chronos'
    msg_count = 0
    while True:
        msg = f'sync_msg'
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send {msg} to topic {topic}")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        time.sleep(10)
        if msg_count > 100:
            break


def run():
    client = mqtt.Client()
    client.connect("localhost",1883,60)
    client.loop_start()
    publish_time(client)
    client.loop_stop()
    
if __name__ == "__main__":
    run()