import paho.mqtt.client as mqtt
import time

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="loggers_file.log", level = logging.DEBUG, format = "%(asctime)s:%(levelname)s%(name)s:%(message)s")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Publisher Client is connected")
        global connected
        connected = True
    else:
        logger.info(f"Publisher Connection Failed with code {rc}")

def on_publish(client, userdata, mid):
    global published_message
    logger.info(f"Published Messaged : {published_message}")



connected = False
broker_address = "localhost"
port = 1883
user = "laptop1"

client = mqtt.Client(client_id="Publisher")
client.username_pw_set(username=user, password=None)
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker_address, port=port)

client.loop_start()

while not connected:
    time.sleep(1)


time.sleep(2)
published_message = "I am currently staying in Hyderabad"
client.publish("mqtt/firstcode",published_message)
time.sleep(5)

client.loop_stop()
client.disconnect()
