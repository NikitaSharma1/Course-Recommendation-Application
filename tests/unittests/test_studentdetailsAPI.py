import pytest
from main import app
from application.database import db



def test_studentdetails_api_post(client,db_init):
    #Act
    data={
        "user_id": 1,
        "roll_no": "22f1000888",
        "current_status": "Enrolled",
        "select_your_course": "PDSA",
        "commit_per_week": 30,
        "budget_per_term": 30000,
        "CGPA": 8.5,
        "interest": "Programming",
        "about": "A passionate student",
        "dob": "2000-01-01"
        }
    response = client.post('/api/studentdetails', json=data)

    #Assertion
    assert response.status_code==200


def test_studentdetails_api_get(client,db_init):
    #Act
    response = client.get('/api/studentdetails')
    
    #Assertion
    assert response.status_code==200
    assert response.json[0]['user_id']==1
    assert response.json[0]['roll_no']=='22f1000888'
    assert response.json[0]['current_status']=='Enrolled'
    assert response.json[0]['select_your_course']=='PDSA'
    assert response.json[0]['commit_per_week']==30
    assert response.json[0]['budget_per_term']==30000
    assert response.json[0]['CGPA']==8.5
    assert response.json[0]['interest']=='Programming'
    assert response.json[0]['about']=='A passionate student'


def test_studentdetails_api_put(client,db_init):
    #Act
    data={
        "user_id": 1,
        "roll_no": "22f1000898",
        "current_status": "Enrolled",
        "select_your_course": "PDSA",
        "commit_per_week": 30,
        "budget_per_term": 30000,
        "CGPA": 8.5,
        "interest": "Programming",
        "about": "A passionate student",
        "dob": "2000-01-01"
        }
    response = client.put('/api/studentdetails/1', json=data)

    #Assertion
    assert response.status_code==200
    assert response.json['roll_no']=='22f1000898'


def test_studentdetails_api_delete(client,db_init):
    #Act
    response = client.delete('/api/studentdetails/1')

    #Assertion
    assert response.status_code==200
    assert response.json['message']=='Student details deleted successfully'


def test_studentdetails_api_post_norollno(client,db_init):
    #Act
    data={
        "user_id": 1,
        "current_status": "Enrolled",
        "select_your_course": "PDSA",
        "commit_per_week": 30,
        "budget_per_term": 30000,
        "CGPA": 8.5,
        "interest": "Programming",
        "about": "A passionate student",
        "dob": "2000-01-01"
        }
    response = client.post('/api/studentdetails', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_message']=='roll_no is required'


def test_studentdetails_api_post_nocurrentstatus(client,db_init):
    #Act
    data={
        "user_id": 1,
        "roll_no": "22f1000888",
        "select_your_course": "PDSA",
        "commit_per_week": 30,
        "budget_per_term": 30000,
        "CGPA": 8.5,
        "interest": "Programming",
        "about": "A passionate student",
        "dob": "2000-01-01"
        }
    response = client.post('/api/studentdetails', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_message']=='current_status is required'


def test_studentdetails_api_post_nocourse(client,db_init):
    #Act
    data={
        "user_id": 1,
        "roll_no": "22f1000888",
        "current_status": "Enrolled",
        "commit_per_week": 30,
        "budget_per_term": 30000,
        "CGPA": 8.5,
        "interest": "Programming",
        "about": "A passionate student",
        "dob": "2000-01-01"
        }
    response = client.post('/api/studentdetails', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_message']=='select_your_course is required'


def test_studentdetails_api_post_nocommit(client,db_init):
    #Act
    data={
        "user_id": 1,
        "roll_no": "22f1000888",
        "current_status": "Enrolled",
        "select_your_course": "PDSA",
        "budget_per_term": 30000,
        "CGPA": 8.5,
        "interest": "Programming",
        "about": "A passionate student",
        "dob": "2000-01-01"
        }
    response = client.post('/api/studentdetails', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_message']=='commit_per_week is required'


def test_studentdetails_api_post_nobudget(client,db_init):
    #Act
    data={
        "user_id": 1,
        "roll_no": "22f1000888",
        "current_status": "Enrolled",
        "select_your_course": "PDSA",
        "commit_per_week": 30,
        "CGPA": 8.5,
        "interest": "Programming",
        "about": "A passionate student",
        "dob": "2000-01-01"
        }
    response = client.post('/api/studentdetails', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_message']=='budget_per_term is required'


def test_studentdetails_api_post_nocgpa(client,db_init):
    #Act
    data={
        "user_id": 1,
        "roll_no": "22f1000888",
        "current_status": "Enrolled",
        "select_your_course": "PDSA",
        "commit_per_week": 30,
        "budget_per_term": 30000,
        "interest": "Programming",
        "about": "A passionate student",
        "dob": "2000-01-01"
        }
    response = client.post('/api/studentdetails', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_message']=='CGPA is required'


def test_studentdetails_api_post_nointerest(client,db_init):
    #Act
    data={
        "user_id": 1,
        "roll_no": "22f1000888",
        "current_status": "Enrolled",
        "select_your_course": "PDSA",
        "commit_per_week": 30,
        "budget_per_term": 30000,
        "CGPA": 8.5,
        "about": "A passionate student",
        "dob": "2000-01-01"
        }
    response = client.post('/api/studentdetails', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_message']=='interest is required'


def test_studentdetails_api_post_noabout(client,db_init):
    #Act
    data={
        "user_id": 1,
        "roll_no": "22f1000888",
        "current_status": "Enrolled",
        "select_your_course": "PDSA",
        "commit_per_week": 30,
        "budget_per_term": 30000,
        "CGPA": 8.5,
        "interest": "Programming",
        "dob": "2000-01-01"
        }
    response = client.post('/api/studentdetails', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_message']=='about is required'


def test_studentdetails_api_post_nodob(client,db_init):
    #Act
    data={
        "user_id": 1,
        "roll_no": "22f1000888",
        "current_status": "Enrolled",
        "select_your_course": "PDSA",
        "commit_per_week": 30,
        "budget_per_term": 30000,
        "CGPA": 8.5,
        "interest": "Programming",
        "about": "A passionate student"
        }
    response = client.post('/api/studentdetails', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_message']=='dob is required'


def test_studentdetails_api_post_detailsexist(client,db_init):
    #Act
    data={
        "user_id": 1,
        "roll_no": "22f1000888",
        "current_status": "Enrolled",
        "select_your_course": "PDSA",
        "commit_per_week": 30,
        "budget_per_term": 30000,
        "CGPA": 8.5,
        "interest": "Programming",
        "about": "A passionate student",
        "dob": "2000-01-01"
        }
    response = client.post('/api/studentdetails', json=data)
    response = client.post('/api/studentdetails', json=data)

    #Assertion
    assert response.status_code==400
    assert response.json['error_message']=='student details already exist'