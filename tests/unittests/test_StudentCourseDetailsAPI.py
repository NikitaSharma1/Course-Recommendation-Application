import pytest
from main import app
from application.database import db
from application.api.StudentCourseDetailsAPI import StudentCourseDetailsAPI
from datetime import datetime

def test_student_course_details_api_post(client, db_init):
    # Arrange
    data = {
        "roll_no": "123",
        "course_id": "CS101",
        "course_term": "Fall 2021",
        "course_status": "Completed",
        "grade": "A"
    }

    # Act
    response = client.post('/api/studentcoursedetails', json=data)

    # Assertion
    assert response.status_code == 200
    assert response.json['roll_no'] == "123"
    assert response.json['course_id'] == "CS101"
    assert response.json['course_term'] == "Fall 2021"
    assert response.json['course_status'] == "Completed"
    assert response.json['grade'] == "A"

def test_student_course_details_api_get(client, db_init):
    # Act
    response = client.get('/api/studentcoursedetails')

    # Assertion
    assert response.status_code == 200

def test_student_course_details_api_put(client, db_init):
    # Arrange
    data = {
        "roll_no": "123",
        "course_id": "CS101",
        "course_term": "Fall 2021",
        "course_status": "Completed",
        "grade": "A"
    }

    # Act
    response = client.put('/api/studentcoursedetails/1', json=data)

    # Assertion
    assert response.status_code == 200
    assert response.json['roll_no'] == "123"
    assert response.json['course_id'] == "CS101"
    assert response.json['course_term'] == "Fall 2021"
    assert response.json['course_status'] == "Completed"
    assert response.json['grade'] == "A"

def test_student_course_details_api_post_missing_fields(client, db_init):
    # Arrange
    data = {
        "roll_no": "123",
        "course_id": "CS101",
        # Missing course_term, course_status, and grade
    }

    # Act
    response = client.post('/api/studentcoursedetails', json=data)

    # Assertion
    assert response.status_code == 400
    assert 'error_code' in response.json
    assert response.json['error_code'] == "SCD003"  # course_term is required

def test_student_course_details_api_put_missing_fields(client, db_init):
    # Arrange
    data = {
        "roll_no": "123",
        "course_id": "CS101",
        # Missing course_term, course_status, and grade
    }

    # Act
    response = client.put('/api/studentcoursedetails/1', json=data)

    # Assertion
    assert response.status_code == 400
    assert 'error_code' in response.json
    assert response.json['error_code'] == "SCD003"  # course_term is required

def test_student_course_details_api_put_nonexistent_record(client, db_init):
    # Arrange
    data = {
        "roll_no": "123",
        "course_id": "CS101",
        "course_term": "Fall 2021",
        "course_status": "Completed",
        "grade": "A"
    }

    # Act
    response = client.put('/api/studentcoursedetails/999', json=data)  # Nonexistent record id

    # Assertion
    assert response.status_code == 404

def test_student_course_details_api_delete_nonexistent_record(client, db_init):
    # Act
    response = client.delete('/api/studentcoursedetails/999')  # Nonexistent record id

    # Assertion
    assert response.status_code == 404

def test_student_course_details_api_delete(client, db_init):
    # Act
    response = client.delete('/api/studentcoursedetails/1')

    # Assertion
    assert response.status_code == 200