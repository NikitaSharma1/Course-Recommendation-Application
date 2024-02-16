import pytest
from main import app
from application.database import db



def test_courses_api(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 10000,
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==200
    assert response.json['course_name'] == "PDSA"
    assert response.json['level'] == "Diploma"

def test_courses_api_get(client,db_init):
    #Act
    response = client.get('/api/courses')

    #Assertion
    assert response.status_code==200
    assert response.json[0]['course_name'] == "PDSA"
    assert response.json[0]['level'] == "Diploma"


def test_courses_api_put(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 10000,
        "course_credit": 4,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 10000,
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90
        }
    
    response = client.put('/api/courses/1', json=data)

    #Assertion
    assert response.status_code==200
    assert response.json['course_name'] == "PDSA"
    assert response.json['level'] == "Diploma"
    assert response.json['enrolled_so_far'] == 10000

def test_courses_api_delete(client,db_init):
    #Act
    response = client.delete('/api/courses/1')

    #Assertion
    assert response.status_code==200
    assert response.json['message'] == "Course deleted successfully"

def test_courses_api_nocoursename(client,db_init):
    #Act
    data={
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 10000,
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C002"
    assert response.json['error_message'] == "course_name is required"
 
def test_courses_api_nolevel(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 10000,
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C003"
    assert response.json['error_message'] == "level is required"


def test_courses_api_noenrolled_this_term(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 10000,
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C004"
    assert response.json['error_message'] == "enrolled_this_term is required"  


def test_courses_api_noenrolled_so_far(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "course_credit": 4,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 10000,
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C005"
    assert response.json['error_message'] == "enrolled_so_far is required"


def test_courses_api_nocourse_credit(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 10000,
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C006"
    assert response.json['error_message'] == "course_credit is required"


def test_courses_api_nocourse_description(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 10000,
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C007"
    assert response.json['error_message'] == "course_description is required"


def test_courses_api_noteacher(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "course_description": "programming",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 10000,
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C008"
    assert response.json['error_message'] == "teacher is required"


def test_courses_api_nopre_req1(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req2": "DBMS",
        "fees": 10000,
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C009"
    assert response.json['error_message'] == "pre_req1 is required"


def test_courses_api_nopre_req2(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "fees": 10000,
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C010"
    assert response.json['error_message'] == "pre_req2 is required"


def test_courses_api_nofees(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90,
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C011"
    assert response.json['error_message'] == "fees is required"


def test_courses_api_notoughness(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 10000,
        "avg_marks": 85.5,
        "success_rate": 90
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C012"
    assert response.json['error_message'] == "toughness is required"


def test_courses_api_noavg_marks(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 10000,
        "toughness": 8,
        "success_rate": 90
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C013"
    assert response.json['error_message'] == "avg_marks is required"


def test_courses_api_nosuccess_rate(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Diploma",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "course_description": "programming",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 10000,
        "toughness": 8,
        "avg_marks": 85.5
        }
    
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C014"
    assert response.json['error_message'] == "success_rate is required"


def test_courses_api_coursealreadyexist(client,db_init):
    #Act
    data={
        "course_name": "PDSA",
        "level": "Degree",
        "enrolled_this_term": 5000,
        "enrolled_so_far": 20000,
        "course_credit": 4,
        "course_description": "data structures",
        "teacher": "John Doe",
        "pre_req1": "NIL",
        "pre_req2": "DBMS",
        "fees": 20000,
        "toughness": 8,
        "avg_marks": 85.5,
        "success_rate": 90
        }

    response = client.post('/api/courses', json=data)
    response = client.post('/api/courses', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code'] == "C015"
    assert response.json['error_message'] == "course already exist"