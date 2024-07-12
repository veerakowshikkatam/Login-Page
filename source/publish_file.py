import paho.mqtt.client as mqtt
import time
from source.logs import logger

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Host server is connected to the broker")
        global connected
        connected = True
    else:
        logger.error(f"Publisher Connection Failed with code {rc}")

def on_publish(client, userdata, mid):
    logger.info(f"Message is published")

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
