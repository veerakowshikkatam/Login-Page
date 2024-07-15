import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from pytest_mock_resources import create_mysql_fixture
from sqlalchemy.orm import declarative_base
from source.database2 import Person, Courses, db
from source.app2 import app

Base = declarative_base()
mysql = create_mysql_fixture(Base, session=True)

@pytest.fixture
def dbsession(mysql):
    session = mysql()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def client():
    with patch.dict(app.config, {
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
        'SERVER_NAME': 'localhost:5000',
        'APPLICATION_ROOT': '/',
        'PREFERRED_URL_SCHEME': 'http'
    }):
        with app.app_context():
            db.create_all()
            with app.test_client() as client:
                yield client
            db.drop_all()

@pytest.fixture
def mqtt_message():
    class MockMQTTMessage:
        def __init__(self, payload, topic):
            self.payload = payload
            self.topic = topic
    return MockMQTTMessage

@pytest.fixture
def mqtt_client():
    with patch('paho.mqtt.client.Client') as MockMQTTClient:
        mock_client = MockMQTTClient.return_value
        mock_client.connect = MagicMock()
        mock_client.subscribe = MagicMock()
        mock_client.loop_start = MagicMock()
        mock_client.loop_stop = MagicMock()
        mock_client.loop_forever = MagicMock()
        yield mock_client

@pytest.fixture
def mock_mqtt_client():
    with patch('source.subscribe.mqtt.Client') as MockMQTTClient:
        mock_client = MockMQTTClient.return_value
        mock_client.connect = MagicMock()
        mock_client.subscribe = MagicMock()
        mock_client.loop_start = MagicMock()
        mock_client.loop_stop = MagicMock()
        mock_client.loop_forever = MagicMock()
        yield mock_client

@pytest.fixture
def new_user():
    user = Person("Koows", "123435", 4)
    return user

@pytest.fixture
def new_course():
    course = Courses("Safety and Security", 40500)
    return course

@pytest.fixture
def users_info():
    data = {
        "username": "Kowsh",
        "password": "kkkokokok",
        "course_id": 2
    }
    return data

@pytest.fixture
def courses_info():
    data = {
        "course_name": "SQL",
        "course_fees": 45000
    }
    return data
