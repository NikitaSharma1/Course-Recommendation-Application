from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.validation import NotGivenError, NotFoundError
from application.models import User,Role,Rolesusers,StudentDetails
from application.database import db
from flask import current_app as app, jsonify
from flask_security import current_user, roles_required,auth_required,hash_password
from sqlalchemy import or_,and_
from itertools import permutations
import datetime

user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "password": fields.String,
}

user_parse = reqparse.RequestParser()
user_parse.add_argument("user_name")
user_parse.add_argument("email")
user_parse.add_argument("password")

def user_to_json(user):
    return {
        "user_name": user.username,
        "email":user.email
    }



def generate_roll_number():
    # Get the current year
    current_year = datetime.datetime.now().year % 100

    # Get the current quarter (assuming it's based on the calendar year)
    current_month = datetime.datetime.now().month
    if current_month in range(1, 5):
        quarter = "f1"
    elif current_month in range(5, 9):
        quarter = "f2"
    else:
        quarter = "f3"

    # Generate the roll number prefix
    roll_number_prefix = f"{current_year:02d}{quarter}"

    # Count the number of existing roll numbers with the same prefix
    existing_count = StudentDetails.query.filter(StudentDetails.roll_no.like(f"{roll_number_prefix}%")).count()

    # Generate the last 6 digits by adding 1 to the existing count
    last_six_digits = str(existing_count + 1).zfill(6)

    # Combine the prefix and last 6 digits to get the final roll number
    roll_number = f"{roll_number_prefix}{last_six_digits}"

    return roll_number





class UserAPI(Resource):
    def get(self):
        users=User.query.all()
        us=[user_to_json(i) for i in users]
        return jsonify(us)

    
    @auth_required('token')
    def put(self):
        args = user_parse.parse_args()
        pswd = args.get("password")


        if pswd is None:
            raise NotGivenError(
                status_code=400,
                error_code="USER003",
                error_message="Password is required",
            )

       
        us = User.query.filter_by(id=current_user.id).first()
        if us:
            us.password = pswd
            db.session.commit()
            return jsonify({"message":"Password changed successfully!!"})

        else:
            raise NotFoundError(status_code=404)
        
    
    def delete(self, user_id):
        us = User.query.filter_by(id=user_id).first()
        if us:
            db.session.delete(us)
            db.session.commit()
            return 200

        else:
            raise NotFoundError(status_code=404)

    
    def post(self):
        args = user_parse.parse_args()
        user_name = args.get("user_name")
        email = args.get("email")
        pswd = args.get("password")

        if user_name is None:
            raise NotGivenError(
                status_code=400,
                error_code="USER001",
                error_message="User_name is required",
            )

        if email is None:
            raise NotGivenError(
                status_code=400,
                error_code="USER002",
                error_message="Email is required",
            )

        if pswd is None:
            raise NotGivenError(
                status_code=400,
                error_code="USER003",
                error_message="Password is required",
            )

        us = User.query.filter(
            or_(User.username == user_name, User.email == email)
        ).first()
        if us:
            raise NotFoundError(status_code=409)

        else:
            with app.app_context():
                user_datastore = app.security.datastore
                if not user_datastore.find_user(username=user_name) and not user_datastore.find_user(email=email):
                    user_datastore.create_user(username=user_name, email=email, password=hash_password(pswd))
                    db.session.commit()
                    user=User.query.filter_by(email=email).first()
                    role=Rolesusers(user_id=user.id,role_id=2)
                    db.session.add(role)
                    db.session.commit()
                    student=StudentDetails(roll_no=generate_roll_number(),user_id=user.id)
                    db.session.add(student)
                    db.session.commit()

            return {"message":"successfully registered!!"}, 201
        