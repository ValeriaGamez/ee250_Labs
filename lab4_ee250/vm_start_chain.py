import paho.mqtt.client as mqtt
import time


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("vgamez/pong")

def on_message(client, userdata, message):
    received_number = int(message.payload.decode())
    print("Start Received:", received_number)
    new_number = received_number + 1
    print("Start Published:", new_number)
    time.sleep(1)
    client.publish("vgamez/ping", new_number)

if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

    client.on_message = on_message
    client.on_connect = on_connect

   
    client.connect(host="172.20.10.10")

    #client.subscribe("vgamez/pong")

    #client.loop_start()

    # Publish a message with an integer number as payload to the topic "YOUR_USERNAME/ping"
    number = 0
    time.sleep(1)
    print('publishing', number)
    client.publish("vgamez/ping", number)
    

    
    client.loop_forever()


