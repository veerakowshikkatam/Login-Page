import paho.mqtt.client as mqtt
import time
import json
from database2 import Person, session
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename="loggers_file.log", level = logging.DEBUG, format = "%(asctime)s:%(levelname)s%(name)s:%(message)s")


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Subscriber Client is connected")
        client.subscribe("post")
        client.subscribe("put")
        client.subscribe("delete")
    else:
        logger.error(f"Subscriber Connection Failed with code {rc}")

def post_check(message):
    message1 = message.payload.decode()
    data = json.loads(message1)
    username = data["username"]
    password = data["password"]

    existing_user = session.query(Person).filter_by(username = username).first()
    if existing_user:
        logger.warning("Username already taken. Please try new username")
    else:
        new_user = Person(username = username, password = password)
        session.add(new_user)
        session.commit()
        logger.info(f"New User '{username}' successfully added to the database")

def put_check(message):
    message1 = message.payload.decode()
    data = json.loads(message1)
    username = data["username"]
    password = data["password"]

    existing_user = session.query(Person).filter_by(username = username).first()
    if existing_user:
        if existing_user.password == password:
            logger.warning("Password is Matching again. Please try new password")
        else:
            new_user = Person(username = username, password = password)
            session.delete(existing_user)
            session.add(new_user)
            session.commit()
            logger.info("Password is Changed successfully. PUT request is done")
    else:
        logger.warning("Username not found in the database")

def delete_check(message):
    message1 = message.payload.decode()
    data = json.loads(message1)
    username = data["username"]
    password = data["password"]

    existing_user = session.query(Person).filter_by(username = username).first()
    if existing_user:
        if existing_user.password == password:
            session.delete(existing_user)
            session.commit()
            logger.info(f"User '{username}' deleted successfully")
        else:
            logger.warning("Password is not matching, please try again")
    else:
        logger.warning("User not found in database")

def on_message(client, userdata, message):
    logger.info(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")
    if message.topic == "post":
        post_check(message)
    if message.topic == "put":
        put_check(message)
    if message.topic == "delete":
        delete_check(message)

broker_address = "localhost"
port = 1883
user = "laptop1"

client = mqtt.Client(client_id="Subscriber")
client.username_pw_set(username=user, password=None)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=port)

client.loop_forever()