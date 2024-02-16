import pytest
from main import app
from application.database import db



def test_create_feedback_api(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "course_id":1,
        "teacher":1,
        "assignment":1,
        "exams":"test",
        "content":1,
        "toughness":1,
        "overall":1,
        "grade":"A",
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }
    response = client.post('/api/feedback', json=feedback)

    #Assertion
    assert response.status_code==201
    assert response.json['feedback']=='testfeedback'



def test_get_feedback_api(client,db_init):
    #Act
    response = client.get('/api/feedback')

    #Assertion
    assert response.status_code==200
    assert response.json[0]['feedback']=='testfeedback'

def test_delete_feedback_api(client,db_init):
    #Act
    response = client.delete('/api/feedback/1')

    #Assertion
    assert response.status_code==200

def test_update_feedback_api(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "course_id":1,
        "teacher":1,
        "assignment":1,
        "exams":"test",
        "content":1,
        "toughness":1,
        "overall":1,
        "grade":"A",
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }
    response = client.post('/api/feedback',json=feedback)

    #Assertion
    assert response.status_code==201
    assert response.json['feedback']=='testfeedback'

    feedback_update={
        "roll_no":"22f1000888",
        "course_id":1,
        "teacher":1,
        "assignment":1,
        "exams":"test",
        "content":1,
        "toughness":1,
        "overall":1,
        "grade":"A",
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }

    response = client.put('/api/feedback/1',json=feedback_update)
    assert response.status_code==200
    assert response.json['feedback_question']=='testquestion'



def test_post_feedback_api_norollno(client,db_init):
    #Act
    feedback={
        "course_id":1,
        "teacher":1,
        "assignment":1,
        "exams":"test",
        "content":1,
        "toughness":1,
        "overall":1,
        "grade":"A",
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }
    response = client.post('/api/feedback', json=feedback)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="FB001"
    assert response.json['error_message']=='roll_no is required'

def test_post_feedback_api_nocourseid(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "teacher":1,
        "assignment":1,
        "exams":"test",
        "content":1,
        "toughness":1,
        "overall":1,
        "grade":"A",
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }
    response = client.post('/api/feedback', json=feedback)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="FB002"
    assert response.json['error_message']=='course_id is required'

def test_post_feedback_api_noteacher(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "course_id":1,
        "assignment":1,
        "exams":"test",
        "content":1,
        "toughness":1,
        "overall":1,
        "grade":"A",
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }
    response = client.post('/api/feedback', json=feedback)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="FB003"
    assert response.json['error_message']=='teacher is required'

def test_post_feedback_api_noassignment(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "course_id":1,
        "teacher":1,
        "exams":"test",
        "content":1,
        "toughness":1,
        "overall":1,
        "grade":"A",
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }
    response = client.post('/api/feedback', json=feedback)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="FB004"
    assert response.json['error_message']=='assignment is required'

def test_post_feedback_api_noexams(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "course_id":1,
        "teacher":1,
        "assignment":1,
        "content":1,
        "toughness":1,
        "overall":1,
        "grade":"A",
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }
    response = client.post('/api/feedback', json=feedback)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="FB005"
    assert response.json['error_message']=='exams is required'

def test_post_feedback_api_nocontent(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "course_id":1,
        "teacher":1,
        "assignment":1,
        "exams":"test",
        "toughness":1,
        "overall":1,
        "grade":"A",
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }
    response = client.post('/api/feedback', json=feedback)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="FB006"
    assert response.json['error_message']=='content is required'

def test_post_feedback_api_notoughness(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "course_id":1,
        "teacher":1,
        "assignment":1,
        "exams":"test",
        "content":1,
        "overall":1,
        "grade":"A",
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }
    response = client.post('/api/feedback', json=feedback)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="FB007"
    assert response.json['error_message']=='toughness is required'

def test_post_feedback_api_nooverall(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "course_id":1,
        "teacher":1,
        "assignment":1,
        "exams":"test",
        "content":1,
        "toughness":1,
        "grade":"A",
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }
    response = client.post('/api/feedback', json=feedback)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="FB008"
    assert response.json['error_message']=='overall is required'

def test_post_feedback_api_nograde(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "course_id":1,
        "teacher":1,
        "assignment":1,
        "exams":"test",
        "content":1,
        "toughness":1,
        "overall":1,
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }
    response = client.post('/api/feedback', json=feedback)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="FB009"
    assert response.json['error_message']=='grade is required'

def test_post_feedback_api_nofeedback_question(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "course_id":1,
        "teacher":1,
        "assignment":1,
        "exams":"test",
        "content":1,
        "toughness":1,
        "overall":1,
        "grade":"A",
        "feedback":"testfeedback"
    }
    response = client.post('/api/feedback', json=feedback)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="FB010"
    assert response.json['error_message']=="feedback_question is required"

def test_post_feedback_api_nofeedback(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "course_id":1,
        "teacher":1,
        "assignment":1,
        "exams":"test",
        "content":1,
        "toughness":1,
        "overall":1,
        "grade":"A",
        "feedback_question":"testquestion"
    }
    response = client.post('/api/feedback', json=feedback)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=="FB011"
    assert response.json['error_message']=="feedback is required"

def test_post_feedback_api_feedbackexist(client,db_init):
    #Act
    feedback={
        "roll_no":"22f1000888",
        "course_id":1,
        "teacher":2,
        "assignment":1,
        "exams":"test",
        "content":1,
        "toughness":1,
        "overall":1,
        "grade":"A",
        "feedback_question":"testquestion",
        "feedback":"testfeedback"
    }

    response = client.post('/api/feedback', json=feedback)
    assert response.status_code==400
    assert response.json['error_code']=="FB012"
    assert response.json['error_message']=="feedback already exist"