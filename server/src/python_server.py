import paho.mqtt.client as paho
import socket

# https://os.mbed.com/teams/mqtt/wiki/Using-MQTT#python-client

# MQTT broker hosted on local machine
mqttc = paho.Client()

# Settings for connection
#host = "10.25.1.145"
host="m14.cloudmqtt.com"
topic= "Mbed/primes"

active_clients = {}

# Callbacks
def on_connect(self, mosq, obj, rc):
    print("Connected rc: " + str(rc))
    mqttc.publish("Mbed/primes", "Handler Connected!")

def on_message(mosq, obj, msg):
    print("[Received] Topic: " + msg.topic + ", Message: " + str(msg.payload) + "\n");

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed OK")

def on_unsubscribe(mosq, obj, mid, granted_qos):
    print("Unsubscribed OK")

def id_recieved(client, userdata, message):
    #Insert id into the database
    print("Recieved id: " + message.payload)

# Set callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_unsubscribe = on_unsubscribe
mqttc.message_callback_add("id", id_recieved)
#mqttc.message_callback_add()

mqttc.username_pw_set("nqmquhjo", password="-XZCDvgyF01d")



# Connect and subscribe
print("Your IP address is:", socket.gethostbyname(socket.gethostname()))
print("Connecting to " + host + "/" + topic)

mqttc.connect(host, port=13029, keepalive=60)
mqttc.subscribe(topic, 2)
mqttc.publish("Mbed/primes", "id 2")

# Loop forever, receiving messages
mqttc.loop_forever()

print("rc: " + str(rc))

