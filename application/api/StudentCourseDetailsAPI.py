from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.validation import NotGivenError, NotFoundError
from application.models import StudentCourseDetails
from application.database import db
from flask import jsonify
from flask_security import auth_required
from sqlalchemy import and_



student_course_details_fields = {
    "id": fields.Integer,
    "roll_no": fields.String,
    "course_id": fields.Integer,
    "course_term": fields.Integer,
    "course_status": fields.String,
    "grade": fields.String,
}

def student_course_details_to_json(student_course_details):
    return {
        "roll_no": student_course_details.roll_no,
        "course_id": student_course_details.course_id,
        "course_term": student_course_details.course_term,
        "course_status": student_course_details.course_status,
        "grade": student_course_details.grade,
    }

student_course_details_parse = reqparse.RequestParser()
student_course_details_parse.add_argument("roll_no")
student_course_details_parse.add_argument("course_id")
student_course_details_parse.add_argument("course_term")
student_course_details_parse.add_argument("course_status")
student_course_details_parse.add_argument("grade")


class StudentCourseDetailsAPI(Resource):
    def get(self):
        student_course_details=StudentCourseDetails.query.all()
        if student_course_details:
            scd=[student_course_details_to_json(i) for i in student_course_details]
            return jsonify(scd)
        else:
            raise NotFoundError(status_code=404)
    
   
    # @auth_required('token')
    def put(self,student_course_details_id):
        args = student_course_details_parse.parse_args()
        roll_no = args.get("roll_no")
        course_id = args.get("course_id")
        course_term = args.get("course_term")
        course_status = args.get("course_status")
        grade = args.get("grade")

        if roll_no is None:
            raise NotGivenError(
                status_code=400,
                error_code="SCD001",
                error_message="roll_no is required",
            )

        if course_id is None:
            raise NotGivenError(
                status_code=400,
                error_code="SCD002",
                error_message="course_id is required",
            )

    
        if course_term is None:
            raise NotGivenError(
                status_code=400,
                error_code="SCD003",
                error_message="course_term is required",
            )

        if course_status is None:
            raise NotGivenError(
                status_code=400,
                error_code="SCD004",
                error_message="course_status is required",
            )

        if grade is None:
            raise NotGivenError(
                status_code=400,
                error_code="SCD005",
                error_message="grade is required",
            )
        
        scd = StudentCourseDetails.query.filter_by(ucd_id=student_course_details_id).first()
        if scd:
            scd.roll_no = roll_no
            scd.course_id = course_id
            scd.course_term = course_term
            scd.course_status = course_status
            scd.grade = grade
            db.session.commit()
            return {
                "roll_no": scd.roll_no,
                "course_id": scd.course_id,
                "course_term": scd.course_term,
                "course_status": scd.course_status,
                "grade": scd.grade,
            }
        
        else:
            raise NotFoundError(status_code=404)
        
    # @auth_required('token')
    def delete(self, student_course_details_id):
        scd = StudentCourseDetails.query.filter_by(ucd_id=student_course_details_id).first()
        if scd:
            db.session.delete(scd)
            db.session.commit()
            return  200

        else:
            raise NotFoundError(status_code=404)
        
    # @marshal_with(student_course_details_fields)
    # @auth_required('token')
    def post(self):
        args = student_course_details_parse.parse_args()
        roll_no = args.get("roll_no")
        course_id = args.get("course_id")
        course_term = args.get("course_term")
        course_status = args.get("course_status")
        grade = args.get("grade")

        if roll_no is None:
            raise NotGivenError(
                status_code=400,
                error_code="SCD001",
                error_message="roll_no is required",
            )

        if course_id is None:
            raise NotGivenError(
                status_code=400,
                error_code="SCD002",
                error_message="course_id is required",
            )


        if course_term is None:
            raise NotGivenError(
                status_code=400,
                error_code="SCD003",
                error_message="course_term is required",
            )

        if course_status is None:
            raise NotGivenError(
                status_code=400,
                error_code="SCD004",
                error_message="course_status is required",
            )

        if grade is None:
            raise NotGivenError(
                status_code=400,
                error_code="SCD005",
                error_message="grade is required",
            )
        scdd= StudentCourseDetails.query.filter(and_(StudentCourseDetails.roll_no==roll_no, StudentCourseDetails.course_id==course_id)).first()
        if scdd:
            raise NotGivenError(
                status_code=400,
                error_code="SCD006",
                error_message="student course details already exist",
            )
        else:
            scd = StudentCourseDetails(
                roll_no=roll_no,
                course_id=course_id,
                course_term=course_term,
                course_status=course_status,
                grade=grade,
            )
            db.session.add(scd)
            db.session.commit()
            return {
                "roll_no": scd.roll_no,
                "course_id": scd.course_id,
                "course_term": scd.course_term,
                "course_status": scd.course_status,
                "grade": scd.grade,
            }
        