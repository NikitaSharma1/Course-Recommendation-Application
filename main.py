import os
from flask import Flask
from flask_restful import Api
from flask_security import Security, SQLAlchemySessionUserDatastore
from application.config import LocalDevelopmentConfig, TestingConfig
from application.database import db
from application.models import User, Role
from flask_cors import CORS



app = None
api = None


def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv("ENV", "development") == "production":
        raise Exception("Currently no production config is setup.")

    elif os.getenv("ENV", "development") == "testing":
        print("start testing")
        app.config.from_object(TestingConfig)
    else:
        print("Staring Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    api = Api(app)
    CORS(app)
    app.app_context().push()
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    app.security = Security(app, user_datastore)
    return app, api


app, api= create_app()

# Import all the controllers so they are loaded
from application.controllers import *

from application.api.UserAPI import UserAPI
api.add_resource(UserAPI, "/api/user/<int:user_id>", "/api/user")

from application.api.FeedbackAPI import FeedbackAPI
api.add_resource(FeedbackAPI, "/api/feedback/<int:feedback_id>", "/api/feedback", "/api/feedback/<string:course_name>")


from application.api.RecommendationAPI import RecommendationAPI
api.add_resource(RecommendationAPI, "/api/recommendation/<int:recommendation_id>", "/api/recommendation")


from application.api.CoursesAPI import CoursesAPI
api.add_resource(CoursesAPI, "/api/courses/<int:course_id>", "/api/courses")


from application.api.StudentDetailsAPI import StudentDetailsAPI
api.add_resource(StudentDetailsAPI, "/api/studentdetails/<int:sd_id>", "/api/studentdetails")

from application.api.StudentCourseDetailsAPI import StudentCourseDetailsAPI
api.add_resource(StudentCourseDetailsAPI, "/api/studentcoursedetails/<int:student_course_details_id>", "/api/studentcoursedetails")


from application.api.StudentEnrolmentAPI import StudentEnrollmentAPI
api.add_resource(StudentEnrollmentAPI, "/api/studentenrollment/<int:se_id>", "/api/studentenrollment")

from application.api.TermAPI import TermAPI
api.add_resource(TermAPI, "/api/term/<int:term_id>", "/api/term")





if __name__ == "__main__":
    db.create_all()
    # Run the Flask app
    app.run(host='0.0.0.0', port=8080)
