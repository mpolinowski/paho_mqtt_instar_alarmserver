# MQTT publisher
import paho.mqtt.client as mqtt
import sys
import json

# Variables
broker = "192.168.2.117"
username = "admin"
password = "!#()*-./?@[]^_{|}<"
port = 1883
timeout = 60
client = "Paho"
as_cameras = "cameras/+/status/alarm/triggered" 
as_instar  = "instar/+/status/alarm/triggered"


#Callback - Broker connection established
def on_connect(client, userdata, flags, rc):
    print("[STATUS] Broker connection established. Status Code: "+str(rc))
    client.subscribe(as_cameras)
    client.subscribe(as_instar)


#Callback - message received from the broker
def on_message(client, userdata, msg):
    MessageReceived = str(msg.payload.decode())
    ValueReceived = json.loads(msg.payload)

    print("[MSG Received] Topic: "+msg.topic+" / Payload: "+MessageReceived+" / Value: "+ValueReceived['val'])

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnect")

try:
    print("Initializing MQTT")
    client = mqtt.Client()
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    client.connect(broker, port, timeout)
    client.loop_forever()
except KeyboardInterrupt:
    print("Paho MQTT client shutdown")
    sys.exit()
