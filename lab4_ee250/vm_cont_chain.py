
import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("vgamez/ping")

def on_message(client, userdata, message):
    received_number = int(message.payload.decode())
    print("Cont Received:", received_number)
    new_number = received_number + 1
    print("Cont Published:", new_number)
    time.sleep(1)
    client.publish("vgamez/pong", new_number)

if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

    client.on_message = on_message
    client.on_connect = on_connect

    client.connect(host="172.20.10.10")

    client.subscribe("vgamez/ping")

    client.loop_forever()


