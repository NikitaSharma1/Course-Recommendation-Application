import pytest
from main import app
from application.database import db
from application.api.TermAPI import TermAPI
from datetime import datetime, timedelta
import json

def test_term_api_get(client, db_init):
    # Act
    response = client.get('/api/term')

    # Assertion
    assert response.status_code == 200

def test_term_api_post(client, db_init):
    # Arrange
    data = {
        "term": "Spring 2022",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=90)).isoformat(),
        "total_student_enrolled": 100,
        "status": "Open"
    }

    # Act
    response = client.post('/api/term', json=data)

    # Assertion
    assert response.status_code == 201
    assert response.json['term'] == "Spring 2022"
    assert response.json['total_student_enrolled'] == 100
    assert response.json['status'] == "Open"

def test_term_api_put(client, db_init):
    # Arrange
    data = {
        "term": "Spring 2022",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=90)).isoformat(),
        "total_student_enrolled": 200,
        "status": "Closed"
    }

    # Act
    response = client.put('/api/term/1', json=data)

    # Assertion
    assert response.status_code == 200
    assert response.json['term'] == "Spring 2022"
    assert response.json['total_student_enrolled'] == 200
    assert response.json['status'] == "Closed"

def test_post_term_missing_fields(client):
    data = {
        "term": "Spring 2022",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=90)).isoformat(),
        "status": "Open"
    }
    response = client.post('/api/term', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400

def test_put_term_not_found(client):
    data = {
        "term": "Spring 2022",
        "start_date": datetime.now().isoformat(),
        "end_date": (datetime.now() + timedelta(days=90)).isoformat(),
        "total_student_enrolled": 200,
        "status": "Closed"
    }
    response = client.put('/api/term/9999', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 404

def test_delete_term_not_found(client):
    response = client.delete('/api/term/9999')
    assert response.status_code == 404


def test_term_api_delete(client, db_init):
    # Act
    response = client.delete('/api/term/1')

    # Assertion
    assert response.status_code == 200