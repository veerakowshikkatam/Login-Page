import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from flask import jsonify
import json
import pytest
from unittest.mock import patch
from source.subscribe import post_check, put_check, delete_check, post_course, put_course, delete_course, on_message
from source.logs import logger
from source.database2 import Person, Courses, db
from source.app2 import app
from conftest import client, dbsession, mqtt_message, mqtt_client, mock_mqtt_client, new_user, new_course, users_info, courses_info
from unittest.mock import patch, MagicMock

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"My name is Kowshik" in response.data

def test_get_user(client):
    response = client.get('/users', follow_redirects=True)
    assert response.status_code == 200
    assert b"This is users page" in response.data

def test_post_user_publish(client, users_info):
    response = client.post('/users', json=users_info, follow_redirects=True)
    assert response.status_code == 200
    assert b"This is users page" in response.data

def test_delete_user_publish(client, users_info):
    response = client.delete('/users', json=users_info, follow_redirects=True)
    assert response.status_code == 200
    assert b"This is users page" in response.data

def test_put_user_publish(client, users_info):
    response = client.put('/users', json=users_info, follow_redirects=True)
    assert response.status_code == 200
    assert b"This is users page" in response.data

def test_post_course_publish(client, courses_info):
    response = client.post('/courses', json=courses_info, follow_redirects=True)
    assert response.status_code == 200
    assert b"This is courses page" in response.data

def test_put_course_publish(client, courses_info):
    response = client.put('/courses', json=courses_info, follow_redirects=True)
    assert response.status_code == 200
    assert b"This is courses page" in response.data

def test_delete_course_publish(client, courses_info):
    response = client.delete('/courses', json=courses_info, follow_redirects=True)
    assert response.status_code == 200
    assert b"This is courses page" in response.data

@pytest.mark.parametrize("rc, should_subscribe", [(0, True), (1, False)])
def test_on_connect(mock_mqtt_client, rc, should_subscribe):
    from source.subscribe import on_connect
    on_connect(mock_mqtt_client, None, None, rc)

    if should_subscribe:
        expected_topics = ["post", "put", "delete", "post1", "put1", "delete1"]
        for topic in expected_topics:
            mock_mqtt_client.subscribe.assert_any_call(topic)
    else:
        mock_mqtt_client.subscribe.assert_not_called()

@pytest.mark.parametrize("topic",["post"])
def test_on_message(mqtt_message, topic):
    mock_logger_info = MagicMock()
    mock_logger_warning = MagicMock()
    logger.info = mock_logger_info
    logger.warning = mock_logger_warning

    from source.subscribe import on_message
    message_data = {
        "username": "test_user",
        "password": "password",
        "course_id": 1
    }
    message_payload = json.dumps(message_data)
    message = mqtt_message(message_payload.encode(), topic)

    mock_client = MagicMock()
    mock_userdata = MagicMock()

    with patch('source.subscribe.post_check') as mock_post_check:
        on_message(mock_client, mock_userdata, message)
        mock_post_check.assert_called_once_with(message)

    expected_log_info = f"Received message '{message.payload.decode()}' on topic '{message.topic}'"
    mock_logger_info.assert_called_once_with(expected_log_info)

    if message.topic not in ["post", "put", "delete", "post1", "put1", "delete1"]:
        mock_logger_warning.assert_called_once_with(f"No handler found for topic '{message.topic}'")


def test_get_course(client):
    # Sample data to return from the mocked query
    new_user1 = Person("kowshik", "hjdfbvdf", 1)
    new_user2 = Person("kerdsh","gshngf", 1)
    db.session.add(new_user1)
    db.session.add(new_user2)
    db.session.commit()

    response = client.get('/course/1')
    assert response.status_code == 200
    response_json = response.get_json()
    expected_json = db.session.query(Person).filter(Person.course_id == 1).all()
    course_json = [course.to_dict() for course in expected_json]
    assert response_json == course_json

@pytest.mark.parametrize("message_data", [{
    "username": "test_user2",
    "password": "password",
    "course_id": 1
}
    , {
        "username": "Koows",
        "password": "kkkokokok",
        "course_id": 2
    }])
def test_post_check(mqtt_client, mqtt_message, client, new_user, message_data):
    message_payload = json.dumps(message_data)
    message = mqtt_message(message_payload.encode(), "post")

    with app.app_context():
        with patch.object(logger, 'info') as mock_info, \
                patch.object(logger, 'warning') as mock_warning, \
                patch.object(logger, 'error') as mock_error:
            db.session.add(new_user)
            db.session.commit()

            response, status_code = post_check(message)

            if status_code == 400:
                assert b"Username already taken" in response.encode()
            elif status_code == 200:
                assert b"New User added successfully" in response.encode()

@pytest.mark.parametrize("message_data", [{
    "username": "test_user2",
    "password": "password",
    "course_id": 1
}, {
    "username": "Koows",
    "password": "123435",
    "course_id": 2
},
    {
        "username": "Koows",
        "password": "kkkoko34",
        "course_id": 2
    }])
def test_put_check(mqtt_client, mqtt_message, new_user, client, message_data):
    message_payload = json.dumps(message_data)
    message = mqtt_message(message_payload.encode(), "put")

    with app.app_context():
        with patch.object(logger, 'info') as mock_info, \
                patch.object(logger, 'warning') as mock_warning, \
                patch.object(logger, 'error') as mock_error:
            db.session.add(new_user)
            db.session.commit()

            response, status_code = put_check(message)

            if status_code == 400:
                assert b"Username not found" in response.encode()
            elif status_code == 404:
                assert b"Password is Matching again" in response.encode()
            elif status_code == 200:
                assert b"Password is Changed successfully" in response.encode()

@pytest.mark.parametrize("message_data", [{
    "username": "test_user2",
    "password": "password",
    "course_id": 1
}, {
    "username": "Koows",
    "password": "123435",
    "course_id": 4
},
    {
        "username": "Koows",
        "password": "kkkoko34",
        "course_id": 2
    }])
def test_delete_check(mqtt_client, mqtt_message, new_user, client, message_data):
    message_payload = json.dumps(message_data)
    message = mqtt_message(message_payload.encode(), "delete")

    with app.app_context():
        with patch.object(logger, 'info') as mock_info, \
                patch.object(logger, 'warning') as mock_warning, \
                patch.object(logger, 'error') as mock_error:
            db.session.add(new_user)
            db.session.commit()

            response, status_code = delete_check(message)

            if status_code == 404:
                assert b"User not found" in response.encode()
            elif status_code == 400:
                assert b"Password or course_id is not matching" in response.encode()
            elif status_code == 200:
                assert b"User deleted successfully" in response.encode()

@pytest.mark.parametrize("message_data", [
    {
    "course_name": "Python Programming",
    "course_fees": 1000},
    {
        "course_name": "Safety and Security",
        "course_fees": 1000}
])
def test_post_course(mqtt_client, mqtt_message, client, new_course, message_data):
    message_payload = json.dumps(message_data)
    message = mqtt_message(message_payload.encode(), "post1")

    with app.app_context():
        with patch.object(logger, 'info') as mock_info, \
                patch.object(logger, 'warning') as mock_warning, \
                patch.object(logger, 'error') as mock_error:
            db.session.add(new_course)
            db.session.commit()
            response, status_code = post_course(message)

            if status_code == 400:
                assert b"Course already in use" in response.encode()
            elif status_code == 200:
                assert b"New Course" in response.encode()

def test_put_course(mqtt_client, mqtt_message, client):
    message_data = {
        "course_name": "Python Programming",
        "course_fees": 1500
    }
    message_payload = json.dumps(message_data)
    message = mqtt_message(message_payload.encode(), "put1")

    with app.app_context():
        with patch.object(logger, 'info') as mock_info, \
                patch.object(logger, 'warning') as mock_warning, \
                patch.object(logger, 'error') as mock_error:
            response, status_code = put_course(message)

            assert status_code == 405
            assert b"Put method is not applicable" in response.encode()

@pytest.mark.parametrize("message_data", [
    {
        "course_name": "Python Programming",
        "course_fees": 1000},
    {
        "course_name": "Safety and Security",
        "course_fees": 1000}
])
def test_delete_course(mqtt_client, mqtt_message, client, message_data, new_course):
    message_payload = json.dumps(message_data)
    message = mqtt_message(message_payload.encode(), "delete1")

    with app.app_context():
        with patch.object(logger, 'info') as mock_info, \
                patch.object(logger, 'warning') as mock_warning, \
                patch.object(logger, 'error') as mock_error:
            db.session.add(new_course)
            db.session.commit()
            response, status_code = delete_course(message)

            if status_code == 404:
                assert b"Course not found" in response.encode()
            elif status_code == 200:
                assert b"Course deleted successfully" in response.encode()
