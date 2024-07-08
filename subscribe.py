import paho.mqtt.client as mqtt
import json
from database2 import Person, db, Courses
from logs import logger
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Subscriber Client is connected")
        for sub in ["post", "put", "delete", "post1", "put1", "delete1"]:
            client.subscribe(sub)
    else:
        logger.error(f"Subscriber Connection Failed with code {rc}")

def post_check(message):
    with app.app_context():
        message1 = message.payload.decode()
        data = json.loads(message1)
        username = data["username"]
        password = data["password"]
        course_id = data["course_id"]

        existing_user = db.session.query(Person).filter_by(username = username).first()
        if existing_user:
            logger.warning("Username already taken. Please try new username")
        else:
            new_user = Person(username = username, password = password, course_id = course_id)
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"New User '{username}' successfully added to the database")

def put_check(message):
    with app.app_context():
        message1 = message.payload.decode()
        data = json.loads(message1)
        username = data["username"]
        password = data["password"]
        course_id = data["course_id"]

        existing_user = db.session.query(Person).filter_by(username = username).first()
        if existing_user:
            if existing_user.password == password:
                logger.warning("Password is Matching again. Please try new password")
            else:
                new_user = Person(username = username, password = password, course_id = course_id)
                db.session.delete(existing_user)
                db.session.add(new_user)
                db.session.commit()
                logger.info("Password is Changed successfully. PUT request is done")
        else:
            logger.warning("Username not found in the database")

def delete_check(message):
    with app.app_context():
        message1 = message.payload.decode()
        data = json.loads(message1)
        username = data["username"]
        password = data["password"]
        course_id = data["course_id"]

        existing_user = db.session.query(Person).filter_by(username = username).first()
        if existing_user:
            if existing_user.password == password and existing_user.course_id == course_id:
                db.session.delete(existing_user)
                db.session.commit()
                logger.info(f"User '{username}' deleted successfully")
            else:
                logger.warning("Password or course_id is not matching, please try again")
        else:
            logger.warning("User not found in database")

def post_course(message):
    with app.app_context():
        message1 = message.payload.decode()
        data = json.loads(message1)
        course_name = data["course_name"]
        course_fees = data["course_fees"]

        existing_course = db.session.query(Courses).filter_by(course_name = course_name).first()
        if existing_course:
            logger.warning("Course already in use. Please try to add new course")
        else:
            new_course = Courses(course_name = course_name, course_fees= course_fees)
            db.session.add(new_course)
            db.session.commit()
            logger.info(f"New Course '{course_name}' successfully added to the database")
def put_course(message):
    logger.warning("Put method is not applicable for the courses")
def delete_course(message):
    with app.app_context():
        message1 = message.payload.decode()
        data = json.loads(message1)
        course_name = data["course_name"]

        existing_course = db.session.query(Courses).filter_by(course_name = course_name).first()
        if existing_course:
            db.session.delete(existing_course)
            db.session.commit()
            logger.info(f"Course '{course_name}' deleted successfully")
        else:
            logger.warning(f"Course not found in database")


def on_message(client, userdata, message):
    logger.info(f"Received message '{message.payload.decode()}' on topic '{message.topic}'")

    topic_actions = {
        "post": post_check,
        "put": put_check,
        "delete": delete_check,
        "post1": post_course,
        "put1": put_course,
        "delete1": delete_course
    }

    if message.topic in topic_actions:
        topic_actions[message.topic](message)
    else:
        logger.warning(f"No handler found for topic '{message.topic}")

broker_address = "localhost"
port = 1883
user = "laptop1"

client = mqtt.Client(client_id="Subscriber")
client.username_pw_set(username=user, password=None)
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port=port)


client.loop_forever()
app.run(port = 5001)