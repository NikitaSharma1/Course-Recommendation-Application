import pytest
from main import app
from application.database import db
from application.models import StudentDetails, Courses, Recommendation
from datetime import datetime



def test_get_recommendation_api(client,db_init):

    #Arrange
    studd = StudentDetails(
    user_id=1,
    roll_no="22f1000888",
    current_status="Enrolled",
    select_your_course="PDSA",
    commit_per_week=30,
    budget_per_term=30000,
    CGPA=8.5,
    interest="Programming",
    about="A passionate student",
    dob=datetime.strptime(str("2000-01-01"), '%Y-%m-%d').date()
        )
    db.session.add(studd)
    db.session.commit()

    course = Courses(
    course_name="PDSA",
    level="UG",
    enrolled_this_term=100,
    enrolled_so_far=100,
    course_credit=4,
    course_description="Data Structures and Algorithms",
    teacher="Prof. ABC",
    pre_req1="DSA",
    pre_req2="None",
    fees=10000,
    toughness=7,
    avg_marks=80,
    success_rate=90
        )
    db.session.add(course)
    db.session.commit()
    #Act
    response = client.get('/api/recommendation')

    #Assertion
    assert response.status_code==200
    # Check the course_name in the response
    assert response.json[1][0]['course_name'] == "PDSA"

    
    
def test_post_recommendation_api(client,db_init):
    recommendation={
    "roll_no":"22f1000888",
    "course_one":"PDSA",
    "course_two":"DBMS",
    "course_three":"MAD I",
    "course_four":"SC",
    "status":"Enrolled"

    }

    response = client.post('/api/recommendation',json=recommendation)
    assert response.status_code==201
    assert response.json['roll_no']=="22f1000888"


def test_delete_recommendation_api(client,db_init):
    
    #Act
    response = client.delete('/api/recommendation/1')

    #Assertion
    assert response.status_code==200
    assert response.json["message"]=="sucessfully deleted"
   
def test_update_recommendation_api(client,db_init):
    #Act
    recommendation={
    "roll_no":"22f1000888",
    "course_one":"PDSA",
    "course_two":"DBMS",
    "course_three":"MAD I",
    "course_four":"SC",
    "status":"Enrolled"

    }

    response = client.post('/api/recommendation',json=recommendation)
    assert response.status_code==201
    assert response.json['roll_no']=="22f1000888"

    recommendation_update={
    "roll_no":"22f1000898",
    "course_one":"PDSA",
    "course_two":"DBMS",
    "course_three":"MAD I",
    "course_four":"SC",
    "status":"Enrolled"

    }

    response = client.put('/api/recommendation/1',json=recommendation_update)
    assert response.status_code==200
    assert response.json['roll_no']=="22f1000898"


def test_post_recommendation_api_norollno(client,db_init):
    #Act
    recommendation={
    "course_one":"PDSA",
    "course_two":"DBMS",
    "course_three":"MAD I",
    "course_four":"SC",
    "status":"Enrolled"

    }

    response = client.post('/api/recommendation', json=recommendation)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="R001"
    assert response.json['error_message']=="roll_no is required"


def test_post_recommendation_api_nocourse(client,db_init):
    #Act
    recommendation={
    "roll_no":"22f1000888",
    "course_two":"DBMS",
    "course_three":"MAD I",
    "course_four":"SC",
    "status":"Enrolled"

    }

    response = client.post('/api/recommendation', json=recommendation)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="R002"
    assert response.json['error_message']=="course_one is required"

def test_post_recommendation_api_nostatus(client,db_init):
    #Act
    recommendation={
    "roll_no":"22f1000888",
    "course_one":"PDSA",
    "course_two":"DBMS",
    "course_three":"MAD I",
    "course_four":"SC",

    }

    response = client.post('/api/recommendation', json=recommendation)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="R006"
    assert response.json['error_message']=="status is required"

def test_post_recommendation_api_recommendationexist(client,db_init):
    #Act
    recommendation={
    "roll_no":"22f1000888",
    "course_one":"PDSA",
    "course_two":"DBMS",
    "course_three":"MAD I",
    "course_four":"SC",
    "status":"Enrolled"

    }

    response = client.post('/api/recommendation', json=recommendation)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="R007"
    assert response.json['error_message']=="recommendation already exist"