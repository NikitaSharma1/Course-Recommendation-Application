from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.validation import NotGivenError, NotFoundError
from application.models import Feedback,StudentDetails,Courses
from application.database import db
from flask import jsonify
from flask_security import roles_required,auth_required,current_user
from sqlalchemy import and_



feedback_fields = {
    "id": fields.Integer,
    "roll_no": fields.String,
    "course_id": fields.Integer,
    "teacher": fields.String,
    "assignment": fields.Integer,
    "exams": fields.Integer,
    "content": fields.Integer,
    "toughness": fields.Integer,
    "overall": fields.Integer,
    "grade": fields.String,
    "feedback_question": fields.String,
    "feedback": fields.String,
}

feedback_parse = reqparse.RequestParser()
feedback_parse.add_argument("subject")
feedback_parse.add_argument("teacher")
feedback_parse.add_argument("assignment")
feedback_parse.add_argument("exams")
feedback_parse.add_argument("content")
feedback_parse.add_argument("toughness")
feedback_parse.add_argument("overall")
feedback_parse.add_argument("grade")
feedback_parse.add_argument("comments")


def feedback_to_json(feedback):
    return {
        "roll_no": feedback.roll_no,
        "course_id":feedback.course_id,
        "teacher":feedback.teacher,
        "assignment":feedback.assignment,
        "exams":feedback.exams,
        "content":feedback.content,
        "toughness":feedback.toughness,
        "overall":feedback.overall,
        "grade":feedback.grade,
        "feedback":feedback.feedback
    }

class FeedbackAPI(Resource):
    def get(self,course_name):
        course_id=Courses.query.filter_by(course_name=course_name).first().course_id
        feedbacks=Feedback.query.filter_by(course_id=course_id).all()
        fb=[feedback_to_json(i) for i in feedbacks]
        return jsonify(fb)
    
    
   
    def put(self,feedback_id):
        args = feedback_parse.parse_args()
        roll_no = args.get("roll_no")
        course_id = args.get("course_id")
        teacher = args.get("teacher")
        assignment = args.get("assignment")
        exams = args.get("exams")
        content = args.get("content")
        toughness = args.get("toughness")
        overall = args.get("overall")
        grade = args.get("grade")
        feedback_question = args.get("feedback_question")
        feedback = args.get("comments")

        if roll_no is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB001",
                error_message="roll_no is required",
            )

        if course_id is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB002",
                error_message="course_id is required",
            )

        if teacher is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB003",
                error_message="teacher is required",
            )

        if assignment is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB004",
                error_message="assignment is required",
            )

        if exams is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB005",
                error_message="exams is required",
            )

        if content is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB006",
                error_message="content is required",
            )

        if toughness is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB007",
                error_message="toughness is required",
            )

        if overall is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB008",
                error_message="overall is required",
            )

        if grade is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB009",
                error_message="grade is required",
            )


        if feedback is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB011",
                error_message="feedback is required",
            )
        
        fb = Feedback.query.filter_by(f_id=feedback_id).first()
        if fb:
            fb.roll_no = roll_no
            fb.course_id = course_id
            fb.teacher = teacher
            fb.assignment = assignment
            fb.exams = exams
            fb.content = content
            fb.toughness = toughness
            fb.overall = overall
            fb.grade = grade
            fb.feedback_question = feedback_question
            fb.feedback = feedback
            db.session.commit()
            return feedback_to_json(fb)

        else:
            raise NotFoundError(status_code=404)
        
    @auth_required('token')
    @roles_required('student')
    def delete(self, feedback_id):
        fb = Feedback.query.filter_by(f_id=feedback_id).first()
        if fb:
            db.session.delete(fb)
            db.session.commit()
            return 200

        else:
            raise NotFoundError(status_code=404)
        
    @marshal_with(feedback_fields)
    @roles_required('student')
    @auth_required('token')
    def post(self):
        user_id=current_user.id
        user=StudentDetails.query.filter_by(user_id=user_id).first()
        args = feedback_parse.parse_args()
        roll_no = user.roll_no
        sub = args.get("subject")
        course_id= Courses.query.filter_by(course_name=sub).first().course_id
        teacher = args.get("teacher")
        assignment = args.get("assignment")
        exams = args.get("exams")
        content = args.get("content")
        toughness = args.get("toughness")
        overall = args.get("overall")
        grade = args.get("grade")
        feedback = args.get("comments")

        if roll_no is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB001",
                error_message="roll_no is required",
            )

        if course_id is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB002",
                error_message="course_id is required",
            )

        if teacher is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB003",
                error_message="teacher is required",
            )

        if assignment is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB004",
                error_message="assignment is required",
            )

        if exams is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB005",
                error_message="exams is required",
            )

        if content is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB006",
                error_message="content is required",
            )

        if toughness is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB007",
                error_message="toughness is required",
            )

        if overall is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB008",
                error_message="overall is required",
            )

        if grade is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB009",
                error_message="grade is required",
            )

       
        if feedback is None:
            raise NotGivenError(
                status_code=400,
                error_code="FB011",
                error_message="feedback is required",
            )
        fbd= Feedback.query.filter(and_(Feedback.roll_no==roll_no, Feedback.feedback==feedback)).first()
        if fbd:
            raise NotGivenError(
                status_code=400,
                error_code="FB012",
                error_message="feedback already exist",
            )
        
        fb = Feedback(
            roll_no=roll_no,
            course_id=course_id,
            teacher=teacher,
            assignment=assignment,
            exams=exams,
            content=content,
            toughness=toughness,
            overall=overall,
            grade=grade,
            feedback=feedback,
        )
        db.session.add(fb)
        db.session.commit()
        return jsonify({"message": "Feedback added successfully"})
