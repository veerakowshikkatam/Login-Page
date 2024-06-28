import json
from flask import Flask, request

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="loggers_file.log", level = logging.DEBUG, format = "%(asctime)s:%(levelname)s%(name)s:%(message)s")

import paho.mqtt.client as mqtt
import time
app = Flask(__name__)

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

@app.route("/", methods = ["GET", "POST", "PUT", "DELETE"])
def home():
    if request.method == "POST":
        info = request.json
        client.publish("post", json.dumps(info))

    if request.method == "PUT":
        info = request.json
        client.publish("put", json.dumps(info))

    if request.method == "DELETE":
        info = request.json
        client.publish("delete", json.dumps(info))

    return "MY Name is Kowshik"

app.run()
