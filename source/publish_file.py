import paho.mqtt.client as mqtt
import time
from source.logs import logger

def on_connect(client, userdata, flags, rc, properties = None):
    if rc == 0:
        logger.info("Host server is connected to the broker")
        global connected
        connected = True
    else:
        logger.error(f"Publisher Connection Failed with code {rc}")

def on_publish(client, userdata, mid):
    logger.info(f"Message successfully published with mid: {mid}")

connected = False
broker_address = "localhost"
port = 1883
user = "laptop1"

client = mqtt.Client(client_id="Publisher")
client.username_pw_set(username=user, password=None)
client.on_connect = on_connect
client.on_publish = on_publish
client.connect(broker_address, port=port)

# Start a loop to handle MQTT network traffic, callbacks, and reconnections
client.loop_start()

# # Example of publishing a message
# topic = "your/topic"
# message = "Hello, MQTT!"
# client.publish(topic, message)
#
# # Wait for a moment before disconnecting (optional)
# time.sleep(2)
#
# # Disconnect from the broker
# client.disconnect()
#
# # Stop the MQTT loop
# client.loop_stop()
#
# # Ensure all network communications are completed before exiting
time.sleep(1)
