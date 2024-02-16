from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.validation import NotGivenError, NotFoundError
from application.models import Term
from application.database import db
from flask import jsonify
from flask_security import auth_required
from datetime import datetime

term_fields = {
    "t_id": fields.Integer,
    "term": fields.String,
    "start_date": fields.DateTime,
    "end_date": fields.DateTime,
    "total_student_enrolled": fields.Integer,
    "status": fields.String,
}

def term_to_json(term):
    return {
        "t_id": term.t_id,
        "term": term.term,
        "start_date": term.start_date.strftime('%d/%m/%Y %I:%M %p'),
        "end_date": term.end_date.strftime('%d/%m/%Y %I:%M %p'),
        "total_student_enrolled": term.total_student_enrolled,
        "status": term.status,
    }

term_parse = reqparse.RequestParser()
term_parse.add_argument("term")
term_parse.add_argument("start_date")
term_parse.add_argument("end_date")
term_parse.add_argument("total_student_enrolled")
term_parse.add_argument("status")


class TermAPI(Resource):
    def get(self):

        term=Term.query.all()
        if term:
            tr=[term_to_json(i) for i in term]
            return jsonify(tr)
        else:
            return jsonify({})
        
    # @marshal_with(term_fields)
    # @auth_required('token')
    def put(self,term_id):
        args = term_parse.parse_args()
        term = args.get("term")
        start_date = args.get("start_date")
        start_date = datetime.strptime(start_date[:-7], '%Y-%m-%dT%H:%M:%S')
        end_date = args.get("end_date")
        end_date = datetime.strptime(end_date[:-7], '%Y-%m-%dT%H:%M:%S')
        total_student_enrolled = args.get("total_student_enrolled")
        status = args.get("status")


        if term is None:
            raise NotGivenError(
                status_code=400,
                error_code="T001",
                error_message="term is required",
            )

        if start_date is None:
            raise NotGivenError(
                status_code=400,
                error_code="T002",
                error_message="start_date is required",
            )

        if end_date is None:
            raise NotGivenError(
                status_code=400,
                error_code="T003",
                error_message="end_date is required",
            )

        if total_student_enrolled is None:
            raise NotGivenError(
                status_code=400,
                error_code="T004",
                error_message="total_student_enrolled is required",
            )

        if status is None:
            raise NotGivenError(
                status_code=400,
                error_code="T005",
                error_message="status is required",
            )
        
        tr = Term.query.filter_by(t_id=term_id).first()
        if tr:
            tr.term = term
            tr.start_date = start_date
            tr.end_date = end_date
            tr.total_student_enrolled = total_student_enrolled
            tr.status = status
            db.session.commit()
            return term_to_json(tr), 200

        else:
            raise NotFoundError(status_code=404)
        

    # @auth_required('token')
    def delete(self, term_id):
        tr = Term.query.filter_by(t_id=term_id).first()
        if tr:
            db.session.delete(tr)
            db.session.commit()
            return  200

        else:
            raise NotFoundError(status_code=404)
        
    # @marshal_with(term_fields)
    # @auth_required('token')
    def post(self): 
        args = term_parse.parse_args()
        term = args.get("term")
        start_date = args.get("start_date")
        start_date = datetime.strptime(start_date[:-7], '%Y-%m-%dT%H:%M:%S')
        end_date = args.get("end_date")
        end_date = datetime.strptime(end_date[:-7], '%Y-%m-%dT%H:%M:%S')
        total_student_enrolled = args.get("total_student_enrolled")
        status = args.get("status")

        if term is None:
            raise NotGivenError(
                status_code=400,
                error_code="T001",
                error_message="term is required",
            )

        if start_date is None:
            raise NotGivenError(
                status_code=400,
                error_code="T002",
                error_message="start_date is required",
            )

        if end_date is None:
            raise NotGivenError(
                status_code=400,
                error_code="T003",
                error_message="end_date is required",
            )

        if total_student_enrolled is None:
            raise NotGivenError(
                status_code=400,
                error_code="T004",
                error_message="total_student_enrolled is required",
            )

        if status is None:
            raise NotGivenError(
                status_code=400,
                error_code="T005",
                error_message="status is required",
            )
        trr= Term.query.filter(Term.term==term).first()
        if trr:
            raise NotGivenError(
                status_code=400,
                error_code="T006",
                error_message="term already exist",
            )
        else:
            tr = Term(
                term=term,
                start_date=start_date,
                end_date=end_date,
                total_student_enrolled=total_student_enrolled,
                status=status,
            )
            db.session.add(tr)
            db.session.commit()
            return term_to_json(tr), 201
        