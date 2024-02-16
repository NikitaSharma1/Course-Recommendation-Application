import pytest
from main import app
from application.database import db

def test_get_student_enrollment_api(client, db_init):
    # Act
    response = client.get('/api/studentenrollment')

    # Assertion
    assert response.status_code == 200

def test_post_student_enrollment_api(client, db_init):
    # Act
    student_enrollment = {
        "term": "Fall 2021",
        "total_students_enrolled": 100,
        "total_registered_students": 80,
        "students_with_full_profile": 70,
        "Average_score": 85,
        "high_sub_rate": 0.8
    }
    response = client.post('/api/studentenrollment', json=student_enrollment)

    # Assertion
    assert response.status_code == 201
    assert response.json['term'] == 'Fall 2021'


def test_put_student_enrollment_api(client, db_init):
    # Act
    student_enrollment_update = {
        "term": "Fall 2021",
        "total_students_enrolled": 120,
        "total_registered_students": 90,
        "students_with_full_profile": 80,
        "Average_score": 88,
        "high_sub_rate": 0.85
    }
    response = client.put('/api/studentenrollment/1', json=student_enrollment_update)

    # Assertion
    assert response.status_code == 200
    assert response.json['total_students_enrolled'] == 120

def test_post_student_enrollment_api_no_term(client, db_init):
    # Act
    student_enrollment = {
        "total_students_enrolled": 100,
        "total_registered_students": 80,
        "students_with_full_profile": 70,
        "Average_score": 85,
        "high_sub_rate": 0.8
    }
    response = client.post('/api/studentenrollment', json=student_enrollment)

    # Assertion
    assert response.status_code == 400
    assert response.json['error_code'] == 'SE001'
    assert response.json['error_message'] == 'term is required'

def test_delete_student_enrollment_api(client, db_init):
    # Act
    response = client.delete('/api/studentenrollment/1')

    # Assertion
    assert response.status_code == 200