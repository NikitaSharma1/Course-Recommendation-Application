from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.validation import NotGivenError, NotFoundError
from application.models import StudentDetails,User
from application.database import db
from flask import jsonify
from flask_security import auth_required,roles_required,current_user
from sqlalchemy import and_
from datetime import datetime

StudentDetails_fields = {
    "sd_id": fields.Integer,
    "user_id": fields.Integer,
    "roll_no": fields.String,
    "current_status": fields.String,
    "select_your_course": fields.String,
    "commit_per_week": fields.Integer,
    "budget_per_term": fields.Integer,
    "CGPA": fields.Integer,
    "interest": fields.String,
    "about": fields.String,
    "dob": fields.String,
}

def studentdetails_to_json(studentdetails,user):
    return {
        "sd_id": studentdetails.sd_id,
        "user_name": user.username,
        "email": user.email,
        "roll_no": studentdetails.roll_no,
        "current_status": studentdetails.current_status,
        "select_your_course": studentdetails.select_your_course,
        "commit_per_week": studentdetails.commit_per_week,
        "budget_per_term": studentdetails.budget_per_term,
        "CGPA": studentdetails.CGPA,
        "interest": studentdetails.interest,
        "about": studentdetails.about,
        "dob": studentdetails.dob,
    }

StudentDetails_parse = reqparse.RequestParser()
StudentDetails_parse.add_argument("sd_id")
StudentDetails_parse.add_argument("user_id")
StudentDetails_parse.add_argument("roll_no")
StudentDetails_parse.add_argument("current_status")
StudentDetails_parse.add_argument("select_your_course")
StudentDetails_parse.add_argument("commit_per_week")
StudentDetails_parse.add_argument("budget_per_term")
StudentDetails_parse.add_argument("CGPA")
StudentDetails_parse.add_argument("interest")
StudentDetails_parse.add_argument("about")
StudentDetails_parse.add_argument("dob")


class StudentDetailsAPI(Resource):

    @auth_required('token')
    def get(self):
        current_user_id=current_user.id
        studentdetails=StudentDetails.query.filter_by(user_id=current_user_id).first()
        user=User.query.filter_by(id=current_user_id).first()
        if studentdetails:
            sd=studentdetails_to_json(studentdetails,user)
            return jsonify(sd)
        else:
            raise NotFoundError(status_code=404)
        
    # @marshal_with(StudentDetails_fields)
    @auth_required('token')
    @roles_required('student')
    def post(self):
        args = StudentDetails_parse.parse_args()
        user_id = current_user.id
        roll_no = StudentDetails.query.filter_by(user_id=user_id).first().roll_no
        current_status = args.get("current_status")
        select_your_course = args.get("select_your_course")
        commit_per_week = args.get("commit_per_week")
        budget_per_term = args.get("budget_per_term")
        CGPA = args.get("CGPA")
        interest = args.get("interest")
        about = args.get("about")
        dob = args.get("dob")
        if dob is not None:
            dob = datetime.strptime(str(dob), '%Y-%m-%d').date()
        if user_id is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD001",
                error_message="user_id is required",
            )

        if roll_no is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD002",
                error_message="roll_no is required",
            )

        if current_status is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD003",
                error_message="current_status is required",
            )

        if select_your_course is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD004",
                error_message="select_your_course is required",
            )

        if commit_per_week is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD005",
                error_message="commit_per_week is required",
            )

        if budget_per_term is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD006",
                error_message="budget_per_term is required",
            )
        
        if CGPA is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD007",
                error_message="CGPA is required",
            )
        if interest is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD008",
                error_message="interest is required",
            )
        
        if about is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD009",
                error_message="about is required",
            )
        if dob is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD010",
                error_message="dob is required",
            )
        sd=StudentDetails.query.filter_by(user_id=user_id).first()
        if sd:
            raise NotGivenError(
                status_code=400,
                error_code="SD011",
                error_message="student details already exist",
            )
        else:
            sd = StudentDetails(
                user_id=user_id,
                roll_no=roll_no,
                current_status=current_status,
                select_your_course=select_your_course,
                commit_per_week=commit_per_week,
                budget_per_term=budget_per_term,
                CGPA=CGPA,
                interest=interest,
                about=about,
                dob=dob,
            )
            db.session.add(sd)
            db.session.commit()
            return {
                "sd_id": sd.sd_id,
                "user_id": sd.user_id,
                "roll_no": sd.roll_no,
                "current_status": sd.current_status,
                "select_your_course": sd.select_your_course,
                "commit_per_week": sd.commit_per_week,
                "budget_per_term": sd.budget_per_term,
                "CGPA": sd.CGPA,
                "interest": sd.interest,
                "about": sd.about,
                "dob": sd.dob.strftime('%d/%m/%Y'),
            }
        
    # @auth_required('token')
    # @roles_required('student')
    def delete(self, sd_id):
        sd = StudentDetails.query.filter_by(sd_id=sd_id).first()
        if sd:
            db.session.delete(sd)
            db.session.commit()
            return {"message":"Student details deleted successfully"},200

        else:
            raise NotFoundError(status_code=404)
        
    # @marshal_with(StudentDetails_fields)
    @auth_required('token')
    @roles_required('student')
    def put(self, sd_id):
        args = StudentDetails_parse.parse_args()
        user_id = current_user.id
        roll_no = StudentDetails.query.filter_by(user_id=user_id).first().roll_no
        current_status = args.get("current_status")
        select_your_course = args.get("select_your_course")
        commit_per_week = args.get("commit_per_week")
        budget_per_term = args.get("budget_per_term")
        CGPA = args.get("CGPA")
        interest = args.get("interest")
        about = args.get("about")
        dob = args.get("dob")
        dob = datetime.strptime(str(dob), '%Y-%m-%d').date()
        if user_id is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD001",
                error_message="user_id is required",
            )

        if roll_no is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD002",
                error_message="roll_no is required",
            )

        if current_status is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD003",
                error_message="current_status is required",
            )

        if select_your_course is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD004",
                error_message="select_your_course is required",
            )

        if commit_per_week is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD005",
                error_message="commit_per_week is required",
            )
        if budget_per_term is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD006",
                error_message="budget_per_term is required",
            )
        
        if CGPA is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD007",
                error_message="CGPA is required",
            )
        if interest is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD008",
                error_message="interest is required",
            )
        

        if dob is None:
            raise NotGivenError(
                status_code=400,
                error_code="SD010",
                error_message="dob is required",
            )
        sd=StudentDetails.query.filter_by(sd_id=sd_id).first()
        if sd:
            sd.user_id=user_id
            sd.roll_no=roll_no
            sd.current_status=current_status
            sd.select_your_course=select_your_course
            sd.commit_per_week=commit_per_week
            sd.budget_per_term=budget_per_term
            sd.CGPA=CGPA
            sd.interest=interest
            sd.about=about
            sd.dob=dob
            db.session.commit()
            return jsonify({"message":"Student details updated successfully"})
        else:
            raise NotFoundError(status_code=404)