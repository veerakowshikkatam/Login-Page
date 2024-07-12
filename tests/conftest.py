import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest, json
from source.database2 import Person, Courses, db
from unittest.mock import MagicMock
from source.app2 import app
from unittest import mock

def mock_subscribe_functions():
    with mock.patch('source.subscribe.on_connect'):
        with mock.patch('source.subscribe.post_check'):
            with mock.patch('source.subscribe.put_check'):
                with mock.patch('source.subscribe.delete_check'):
                    with mock.patch('source.subscribe.post_course'):
                        with mock.patch('source.subscribe.put_course'):
                            with mock.patch('source.subscribe.delete_course'):
                                yield
@pytest.fixture(autouse=True)
def mock_db_session():
    with mock.patch('source.database2.db.session') as mock_session:
        yield mock_session

@pytest.fixture
def client():
    app.config['Testing'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def client_2():
    app.config['TESTING'] = True
    with app.test_client() as client_2:
        with app.app_context():
            db.create_all()
        yield client_2
        with app.app_context():
            db.session.remove()
            db.drop_all()

@pytest.fixture
def mock_mqtt_client():
    with mock.patch('source.subscribe.mqtt.Client') as MockMQTTClient:
        yield MockMQTTClient.return_value
@pytest.fixture
def new_user():
    user = Person("Koows", "123435", 4)
    return user

@pytest.fixture
def new_course():
    course = Courses("Safety and Security", 40500)
    return course

@pytest.fixture(scope="module")
def mqtt_client(mocker):
    mqtt_client = MagicMock()
    mqtt_client.connect.return_value = 0

    mocker.patch("paho.mqtt.client.Client", return_value = mqtt_client)

    return mqtt_client


@pytest.fixture
def users_info():
    data = {
        "username": "Kowsh",
        "password": "kkkokokok",
        "course_id": 2}
    return data

@pytest.fixture
def courses_info():
    data = {
        "course_name" : "SQL",
        "course_fees": 45000}
    return data
