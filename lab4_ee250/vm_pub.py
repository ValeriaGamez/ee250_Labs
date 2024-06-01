"""EE 250L Lab 04 Starter Code
Run vm_sub.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from datetime import datetime
import socket

"""This function (or "callback") will be executed when this client receives 
a connection acknowledgement packet response from the server. """
def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))


if __name__ == '__main__':
    #get IP address
    ip_address=socket.gethostbyname(socket.gethostname())
    """your code here"""
    #create a client object
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
    
    #attach the on_connect() callback function defined above to the mqtt client
    client.on_connect = on_connect
    """Connect using the following hostname, port, and keepalive interval (in 
    seconds). We added "host=", "port=", and "keepalive=" for illustrative 
    purposes. You can omit this in python.
        
    The keepalive interval indicates when to send keepalive packets to the 
    server in the event no messages have been published from or sent to this 
    client. If the connection request is successful, the callback attached to
    `client.on_connect` will be called."""

    client.connect(host="test.mosquitto.org", port=1883, keepalive=60)

    """ask paho-mqtt to spawn a separate thread to handle
    incoming and outgoing mqtt messages."""
    client.loop_start()
    time.sleep(1)

    while True:
        #replace user with your USC username in all subscriptions
        client.publish("vgamez", f"{ip_address}")
        print("Publishing ip address")
        time.sleep(4)

        #get date and time 
        date_time = datetime.now()
    
        #publish date and time in their own topics
        client.publish("Date", str(date_time).split()[0])
        print("publishing Date " + str(date_time).split()[0])
        client.publish("Time", str(date_time).split()[1])
        print("publishing Time " + str(date_time).split()[1])

