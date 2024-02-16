import pytest
from main import app
from application.database import db



def test_create_user_api(client,db_init):
    #Act
    user={
        "user_name":"testuser",
        "email":"testuser@gmail.com",
        "password":"12345678"
    }
    response = client.post('/api/user', json=user)

    #Assertion
    assert response.status_code==201
    assert response.json['user_name']=='testuser'

def test_delete_user_api(client,db_init):
    #Act
    response = client.delete('/api/user/1')

    #Assertion
    assert response.status_code==200
    

def test_update_user_api(client,db_init):
    #Act
    user={
        "user_name":"testuser",
        "email":"testuser@gmail.com",
        "password":"12345678"
    }
    
    response = client.post('/api/user',json=user)

    #Assertion
    assert response.status_code==201
    assert response.json['user_name']=='testuser'

    user_update={
        "user_name":"testuser",
        "email":"test@gmail.com",
        "password":"12345678"
    }

    response = client.put('/api/user/1',json=user_update)
    assert response.status_code==200
    assert response.json['email']=='test@gmail.com'

def test_get_user_api(client,db_init):
    #Act
    response = client.get('/api/user')

    #Assertion
    assert response.status_code==200
    assert response.json[0]['user_name']=='testuser'
    assert response.json[0]['email']=='test@gmail.com'


def test_post_user_api_nousername(client,db_init):
    #Act
    user={
        "email":"test@gmail.com",
        "password":"12345678"
    }
    response = client.post('/api/user', json=user)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=='USER001'
    assert response.json['error_message']=='User_name is required'
    

def test_post_user_api_noemail(client,db_init):
    #Act
    user={
        "user_name":"testuser",
        "password":"12345678"
    }
    response = client.post('/api/user', json=user)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=='USER002'
    assert response.json['error_message']=='Email is required'

def test_post_user_api_nopassword(client,db_init):
    #Act
    user={
        "user_name":"testuser",
        "email":"test@gmail.com"
    }
    response = client.post('/api/user', json=user)

    #Assertion
    assert response.status_code==400
    assert response.json['error_code']=='USER003'
    assert response.json['error_message']=='Password is required'


def test_post_user_api_userexist(client,db_init):
    #Act
    user={
        "user_name":"testuser",
        "email":"test@gmail.com",
        "password":"12345678"
    }
    response = client.post('/api/user', json=user)

    #Assertion
    assert response.status_code==409
    assert response.json=='already exists'
