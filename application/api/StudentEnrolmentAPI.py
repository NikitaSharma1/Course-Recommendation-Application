from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.validation import NotGivenError, NotFoundError
from application.models import StudentEnrollment
from application.database import db
from flask import current_app as app, jsonify
from flask_security import current_user, roles_required,auth_required,hash_password
from sqlalchemy import or_,and_
from itertools import permutations


StudentEnrollment_fields = {
    "se_id": fields.Integer,
    "term": fields.String,
    "total_students_enrolled": fields.Integer,
    "total_registered_student": fields.Integer,
    "students_with_full_profile": fields.Integer,
    "Average_score": fields.Integer,
    "high_sub_rate": fields.Integer,
}

def studentenrollment_to_json(studenroll):
    return {
        "se_id": studenroll.se_id,
        "term": studenroll.term,
        "total_students_enrolled": studenroll.total_student_enrolled,
        "total_registered_student": studenroll.total_registered_student,
        "students_with_full_profile": studenroll.students_with_full_profile,
        "Average_score": studenroll.Average_score,
        "high_sub_rate": studenroll.high_sub_rate,
    }

StudentEnrollment_parse=reqparse.RequestParser()
StudentEnrollment_parse.add_argument("se_id")
StudentEnrollment_parse.add_argument("term")
StudentEnrollment_parse.add_argument("total_students_enrolled")
StudentEnrollment_parse.add_argument("total_registered_students")
StudentEnrollment_parse.add_argument("students_with_full_profile")
StudentEnrollment_parse.add_argument("Average_score")
StudentEnrollment_parse.add_argument("high_sub_rate")


class StudentEnrollmentAPI(Resource):


    # @auth_required('token')
    def get(self):
        studentenrollment=StudentEnrollment.query.all()
        if studentenrollment:
            se=[studentenrollment_to_json(i) for i in studentenrollment]
            return jsonify(se)
        else:
            return jsonify({})
        
    # @marshal_with(StudentEnrollment_fields)
    # @auth_required('token')
    # @roles_required('student')
    def post(self):
        args = StudentEnrollment_parse.parse_args()
        term = args.get("term")
        total_students_enrolled = args.get("total_students_enrolled")
        total_registered_students = args.get("total_registered_students")
        students_with_full_profile = args.get("students_with_full_profile")
        Average_score = args.get("Average_score")
        high_sub_rate = args.get("high_sub_rate")

        if term is None:
            raise NotGivenError(
                status_code=400,
                error_code="SE001",
                error_message="term is required",
            )

        if total_students_enrolled is None:
            raise NotGivenError(
                status_code=400,
                error_code="SE002",
                error_message="total_students_emrolled is required",
            )

        if total_registered_students is None:
            raise NotGivenError(
                status_code=400,
                error_code="SE003",
                error_message="total_registered_students is required",
            )

        if students_with_full_profile is None:
            raise NotGivenError(
                status_code=400,
                error_code="SE004",
                error_message="students_with_full_profile is required",
            )

        if Average_score is None:
            raise NotGivenError(
                status_code=400,
                error_code="SE005",
                error_message="Average_score is required",
            )

        if high_sub_rate is None:
            raise NotGivenError(
                status_code=400,
                error_code="SE006",
                error_message="high_sub_rate is required",
            )
        se=StudentEnrollment.query.filter_by(term=term).first()
        if se:
            raise NotGivenError(
                status_code=400,
                error_code="SE007",
                error_message="studentenrollment already exist",
            )
        else:
            se = StudentEnrollment(
                term=term,
                total_student_enrolled=total_students_enrolled,
                total_registered_student=total_registered_students,
                students_with_full_profile=students_with_full_profile,
                Average_score=Average_score,
                high_sub_rate=high_sub_rate,
            )
            db.session.add(se)
            db.session.commit()
            return studentenrollment_to_json(se), 201
        
    # @auth_required('token')
    # @roles_required('admin')
    def delete(self, se_id):
        se = StudentEnrollment.query.filter_by(se_id=se_id).first()
        if se:
            db.session.delete(se)
            db.session.commit()
            return 200

        else:
            raise NotFoundError(status_code=404)
    
    # @marshal_with(StudentEnrollment_fields)
    # @auth_required('token')
    # @roles_required('admin')
    def put(self, se_id):
        args = StudentEnrollment_parse.parse_args()
        term = args.get("term")
        total_students_enrolled = args.get("total_students_enrolled")
        total_registered_students = args.get("total_registered_students")
        students_with_full_profile = args.get("students_with_full_profile")
        Average_score = args.get("Average_score")
        high_sub_rate = args.get("high_sub_rate")

        if term is None:
            raise NotGivenError(
                status_code=400,
                error_code="SE001",
                error_message="term is required",
            )

        if total_students_enrolled is None:
            raise NotGivenError(
                status_code=400,
                error_code="SE002",
                error_message="total_students_emrolled is required",
            )

        if total_registered_students is None:
            raise NotGivenError(
                status_code=400,
                error_code="SE003",
                error_message="total_registered_students is required",
            )
        if students_with_full_profile is None:
            raise NotGivenError(
                status_code=400,
                error_code="SE004",
                error_message="students_with_full_profile is required",
            )
        if Average_score is None:
            raise NotGivenError(
                status_code=400,
                error_code="SE005",
                error_message="Average_score is required",
            )
        if high_sub_rate is None:
            raise NotGivenError(
                status_code=400,
                error_code="SE006",
                error_message="high_sub_rate is required",
            )
        se=StudentEnrollment.query.filter_by(se_id=se_id).first()
        if se:
            se.term=term
            se.total_student_enrolled=total_students_enrolled
            se.total_registered_student=total_registered_students
            se.students_with_full_profile=students_with_full_profile
            se.Average_score=Average_score
            se.high_sub_rate=high_sub_rate
            db.session.commit()
            return studentenrollment_to_json(se), 200
        else:
            raise NotFoundError(status_code=404)