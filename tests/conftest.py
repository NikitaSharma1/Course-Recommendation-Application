import pytest
from main import app
from application.database import db

@pytest.fixture(scope="module")
def client():
    #Arrange
    # print("****************GETTING CLIENT***********************")
    client=app.test_client()
    ctx=app.app_context()
    ctx.push()

    #ACT
    yield client

    #Clean-up
    ctx.pop()


@pytest.fixture(scope="module")
def db_init():
    # print("****************GETTING DB***********************")
    #create the database and its tables
    db.create_all()

    yield db #this is where the testing happens

    #Tear-down
    db.drop_all()