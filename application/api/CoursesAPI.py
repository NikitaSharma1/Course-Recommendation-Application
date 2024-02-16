from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.validation import NotGivenError, NotFoundError
from application.models import Courses,StudentCourseDetails
from application.database import db
from flask import jsonify
from flask_security import auth_required,roles_required



course_fields = {
    "course_id": fields.Integer,
    "course_name": fields.String,
    "level": fields.String,
    "enrolled_this_term": fields.Integer,
    "enrolled_so_far": fields.Integer,
    "course_credit": fields.Integer,
    "course_description": fields.String,
    "teacher": fields.String,
    "pre_req1": fields.String,
    "pre_req2": fields.String,
    "fees": fields.Integer,
    "toughness": fields.Integer,
    "avg_marks": fields.Integer,
    "success_rate": fields.Integer,
}

course_parse = reqparse.RequestParser()
course_parse.add_argument("course_id")
course_parse.add_argument("course_name")
course_parse.add_argument("level")
course_parse.add_argument("enrolled_this_term")
course_parse.add_argument("enrolled_so_far")
course_parse.add_argument("course_credit")
course_parse.add_argument("course_description")
course_parse.add_argument("teacher")
course_parse.add_argument("pre_req1")
course_parse.add_argument("pre_req2")
course_parse.add_argument("fees")
course_parse.add_argument("toughness")
course_parse.add_argument("avg_marks")
course_parse.add_argument("success_rate")

def course_to_json(course):
    return {
        "course_id": course.course_id,
        "course_name": course.course_name,
        "level": course.level,
        "enrolled_this_term": course.enrolled_this_term,
        "enrolled_so_far": course.enrolled_so_far,
        "course_credit": course.course_credit,
        "course_description": course.course_description,
        "teacher": course.teacher,
        "pre_req1": course.pre_req1,
        "pre_req2": course.pre_req2,
        "fees": course.fees,
        "toughness": course.toughness,
        "avg_marks": course.avg_marks,
        "success_rate": course.success_rate,
    }



class CoursesAPI(Resource):

    
    def get(self):
        courses=Courses.query.all()
        if courses:
            cs=[course_to_json(i) for i in courses]
            return jsonify(cs)
        else:
            return jsonify({})
        
    
    def post(self):
        args = course_parse.parse_args()
        course_name = args.get("course_name")
        level = args.get("level")
        enrolled_this_term = args.get("enrolled_this_term")
        enrolled_so_far = args.get("enrolled_so_far")
        course_credit = args.get("course_credit")
        course_description = args.get("course_description")
        teacher = args.get("teacher")
        pre_req1 = args.get("pre_req1")
        pre_req2 = args.get("pre_req2")
        fees = args.get("fees")
        toughness = args.get("toughness")
        avg_marks = args.get("avg_marks")
        success_rate = args.get("success_rate")


        if course_name is None:
            raise NotGivenError(
                status_code=400,
                error_code="C002",
                error_message="course_name is required",
            )

        if level is None:
            raise NotGivenError(
                status_code=400,
                error_code="C003",
                error_message="level is required",
            )

        if enrolled_this_term is None:
            raise NotGivenError(
                status_code=400,
                error_code="C004",
                error_message="enrolled_this_term is required",
            )
        if enrolled_so_far is None:
            raise NotGivenError(
                status_code=400,
                error_code="C005",
                error_message="enrolled_so_far is required",
            )
        
        if course_credit is None:
            raise NotGivenError(
                status_code=400,
                error_code="C006",
                error_message="course_credit is required",
            )
        if course_description is None:
            raise NotGivenError(
                status_code=400,
                error_code="C007",
                error_message="course_description is required",
            )
        if teacher is None: 
            raise NotGivenError(
                status_code=400,
                error_code="C008",
                error_message="teacher is required",
            )
        if pre_req1 is None:
            raise NotGivenError(
                status_code=400,
                error_code="C009",
                error_message="pre_req1 is required",
            )
        if pre_req2 is None:
            raise NotGivenError(
                status_code=400,
                error_code="C010",
                error_message="pre_req2 is required",
            )
        if fees is None:
            raise NotGivenError(
                status_code=400,
                error_code="C011",
                error_message="fees is required",
            )
        if toughness is None:
            raise NotGivenError(
                status_code=400,
                error_code="C012",
                error_message="toughness is required",
            )
        
        if avg_marks is None:
            raise NotGivenError(
                status_code=400,
                error_code="C013",
                error_message="avg_marks is required",
            )
        if success_rate is None:
            raise NotGivenError(
                status_code=400,
                error_code="C014",
                error_message="success_rate is required",
            )
        
        cs = Courses.query.filter_by(course_name=course_name).first()
        if cs:
            raise NotGivenError(
                status_code=400,
                error_code="C015",
                error_message="course already exist",
            )
        else:
            cs = Courses(
                course_name=course_name,
                level=level,
                enrolled_this_term=enrolled_this_term,
                enrolled_so_far=enrolled_so_far,
                course_credit=course_credit,
                course_description=course_description,
                teacher=teacher,
                pre_req1=pre_req1,
                pre_req2=pre_req2,
                fees=fees,
                toughness=toughness,
                avg_marks=avg_marks,
                success_rate=success_rate,
            )
            db.session.add(cs)
            db.session.commit()
            return course_to_json(cs)
        
    # @auth_required('token')
    # @roles_required('admin')
    def delete(self, course_id):
        cs = Courses.query.filter_by(course_id=course_id).first()
        if cs:
            student_course_details = StudentCourseDetails.query.filter_by(course_id=course_id).all()
            if student_course_details !=[]:
                for i in student_course_details:
                    db.session.delete(i)
                db.session.commit()
            db.session.delete(cs)
            db.session.commit()
            return {"message":"Course deleted successfully"},200

        else:
            raise NotFoundError(status_code=404)
        
    # @marshal_with(course_fields)
    # @auth_required('token')
    # @roles_required('admin')
    def put(self, course_id):
        args = course_parse.parse_args()
        course_name = args.get("course_name")
        level = args.get("level")
        enrolled_this_term = args.get("enrolled_this_term")
        enrolled_so_far = args.get("enrolled_so_far")
        course_credit = args.get("course_credit")
        course_description = args.get("course_description")
        teacher = args.get("teacher")
        pre_req1 = args.get("pre_req1")
        pre_req2 = args.get("pre_req2")
        fees = args.get("fees")
        toughness = args.get("toughness")
        avg_marks = args.get("avg_marks")
        success_rate = args.get("success_rate")

        if course_id is None:
            raise NotGivenError(
                status_code=400,
                error_code="C001",
                error_message="course_id is required",
            )

        if course_name is None:
            raise NotGivenError(
                status_code=400,
                error_code="C002",
                error_message="course_name is required",
            )

        if level is None:
            raise NotGivenError(
                status_code=400,
                error_code="C003",
                error_message="level is required",
            )

        if enrolled_this_term is None:
            raise NotGivenError(
                status_code=400,
                error_code="C004",
                error_message="enrolled_this_term is required",
            )
        if enrolled_so_far is None:
            raise NotGivenError(
                status_code=400,
                error_code="C005",
                error_message="enrolled_so_far is required",
            )
        
        if course_credit is None:
            raise NotGivenError(
                status_code=400,
                error_code="C006",
                error_message="course_credit is required",
            )
        if course_description is None:
            raise NotGivenError(
                status_code=400,
                error_code="C007",
                error_message="course_description is required",
            )
        if teacher is None: 
            raise NotGivenError(
                status_code=400,
                error_code="C008",
                error_message="teacher is required",
            )
        if pre_req1 is None:
            raise NotGivenError(
                status_code=400,
                error_code="C009",
                error_message="pre_req1 is required",
            )
        if pre_req2 is None:
            raise NotGivenError(
                status_code=400,
                error_code="C010",
                error_message="pre_req2 is required",
            )
        if fees is None:
            raise NotGivenError(
                status_code=400,
                error_code="C011",
                error_message="fees is required",
            )
        if toughness is None:
            raise NotGivenError(
                status_code=400,
                error_code="C012",
                error_message="toughness is required",
            )
        
        if avg_marks is None:
            raise NotGivenError(
                status_code=400,
                error_code="C013",
                error_message="avg_marks is required",
            )
        if success_rate is None:
            raise NotGivenError(
                status_code=400,
                error_code="C014",
                error_message="success_rate is required",
            )
        
        cs = Courses.query.filter_by(course_id=course_id).first()
        if cs:
            cs.course_name = course_name
            cs.level = level
            cs.enrolled_this_term = enrolled_this_term
            cs.enrolled_so_far = enrolled_so_far
            cs.course_credit = course_credit
            cs.course_description = course_description
            cs.teacher = teacher
            cs.pre_req1 = pre_req1
            cs.pre_req2 = pre_req2
            cs.fees = fees
            cs.toughness = toughness
            cs.avg_marks = avg_marks
            cs.success_rate = success_rate
            db.session.commit()
            return jsonify({"message":"Course updated successfully"})
        else:
            raise NotFoundError(status_code=404)