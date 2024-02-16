# FILEPATH: /c:/Users/sahil/IITM SE course recommendation project/milestone-4/tests/unittests/test_queriesAPI.py

import pytest
from main import app
from application.database import db
from application.api.QueriesAPI import QueriesAPI
from datetime import datetime



def test_queries_api_post(client, db_init):
    # Arrange
    data = {
        "roll_no": "123",
        "query": "Test query",
        "reply": "Test reply",
        "status": "Open",
        "date": datetime.now().isoformat()
    }

    # Act
    response = client.post('/api/queries', json=data)

    # Assertion
    assert response.status_code == 200
    assert response.json['roll_no'] == "123"
    assert response.json['query'] == "Test query"
    assert response.json['reply'] == "Test reply"
    assert response.json['status'] == "Open"

def test_queries_api_get(client, db_init):
    # Act
    response = client.get('/api/queries')

    # Assertion
    assert response.status_code == 200

def test_queries_api_put(client, db_init):
    # Arrange
    data = {
        "roll_no": "123",
        "query": "Test query",
        "reply": "Test reply",
        "status": "Open",
        "date": datetime.now().isoformat()
    }

    # Act
    response = client.put('/api/queries/1', json=data)

    # Assertion
    assert response.status_code == 200
    assert response.json['roll_no'] == "123"
    assert response.json['query'] == "Test query"
    assert response.json['reply'] == "Test reply"
    assert response.json['status'] == "Open"

def test_queries_api_post_missing_fields(client, db_init):
    # Arrange
    data = {
        "roll_no": "123",
        "query": "Test query",
        # Missing reply, status, and date
    }

    # Act
    response = client.post('/api/queries', json=data)

    # Assertion
    assert response.status_code == 400
    assert 'error_code' in response.json
    assert response.json['error_code'] == "Q003"  # reply is required

def test_queries_api_put_missing_fields(client, db_init):
    # Arrange
    data = {
        "roll_no": "123",
        "query": "Test query",
        # Missing reply, status, and date
    }

    # Act
    response = client.put('/api/queries/1', json=data)

    # Assertion
    assert response.status_code == 400
    assert 'error_code' in response.json
    assert response.json['error_code'] == "Q003"  # reply is required

def test_queries_api_put_nonexistent_query(client, db_init):
    # Arrange
    data = {
        "roll_no": "123",
        "query": "Test query",
        "reply": "Test reply",
        "status": "Open",
        "date": datetime.now().isoformat()
    }

    # Act
    response = client.put('/api/queries/999', json=data)  # Nonexistent query id

    # Assertion
    assert response.status_code == 404

def test_queries_api_delete_nonexistent_query(client, db_init):
    # Act
    response = client.delete('/api/queries/999')  # Nonexistent query id

    # Assertion
    assert response.status_code == 404

def test_queries_api_delete(client, db_init):
    # Act
    response = client.delete('/api/queries/1')

    # Assertion
    assert response.status_code == 200
