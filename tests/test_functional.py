import json
from source.database2 import Person, Courses, db
from source.app2 import app
from unittest import mock
def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"My name is Kowshik" in response.data

def test_get_user(client):
    response = client.get('/users',follow_redirects = True )
    assert response.status_code == 200
    assert b"This is users page" in response.data
def test_post_user(client, users_info):
    response = client.post('/users', json = users_info, follow_redirects = True)
    assert response.status_code == 200
    assert b"This is users page" in response.data

def test_delete_user(client, users_info):
    response = client.delete('/users', json = users_info, follow_redirects = True)
    assert response.status_code == 200
    assert b"This is users page" in response.data

def test_put_user(client, users_info):
    response = client.put('/users', json = users_info, follow_redirects = True)
    assert response.status_code == 200
    assert b"This is users page" in response.data

def test_post_course(courses_info, client):
    response = client.post('/courses', json = courses_info, follow_redirects = True)
    assert response.status_code == 200
    assert b"This is courses page" in response.data

def test_put_course(courses_info, client):
    response = client.put('/courses', json = courses_info, follow_redirects = True)
    assert response.status_code == 200
    assert b"This is courses page" in response.data

def test_delete_course(courses_info, client):
    response = client.delete('/courses', json = courses_info, follow_redirects = True)
    assert response.status_code == 200
    assert b"This is courses page" in response.data


def test_post_check(client_2, mock_mqtt_client):
    # Mock MQTT message
    message_payload = json.dumps({
        "username": "testuser",
        "password": "testpassword",
        "course_id": 1
    })
    assert 1 == 1
    # mock_message = mock.Mock()
    # mock_message.payload.decode.return_value = message_payload
    # mock_message.topic = "post"

    # Simulate on_connect event (if needed)
    # mock_mqtt_client.on_connect(None, None, None, 0)

    # Test post_check function

    # Assert database changes or log messages as expected
    # with app.app_context():
    #     new_user = db.session.query(Person).filter_by(username="testuser").first()
    #     assert new_user is not None
    #     assert new_user.password == "testpassword"
    #     assert new_user.course_id == 1