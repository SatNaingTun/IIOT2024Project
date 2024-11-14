# MyMMqtt.py
# python 3.11

import random
import time

from paho.mqtt import client as mqtt_client


# broker = 'broker.emqx.io'
# broker='192.168.200.21'
port = 1883
# broker='192.168.1.104'
# topic = "iiot/data"
# Generate a Client ID with the publish prefix.
client_id = f'publish-{random.randint(0, 1000)}'
# username = 'pi'
# password = 'pi'


def connect_mqtt(mqtt_ip, port, username, password):
    """Connect to the MQTT broker and handle connection errors."""
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id=client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    try:
        client.connect(mqtt_ip, port)
    except Exception as e:
        print(f"Could not connect to MQTT Broker: {e}")
        return None
    return client


def publish(client, data, topic):
    # msg_count = 1
    # while True:
    time.sleep(1)
    # msg = f"messages: {msg_count}"
    result = client.publish(topic, data)
    # result: [0, 1]
    status = result[0]


def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run(data):
    client = connect_mqtt()
    client.loop_start()
    publish(client, data)
    client.loop_stop()


if __name__ == '__main__':
    run("test")
