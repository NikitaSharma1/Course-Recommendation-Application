from flask_security import UserMixin, RoleMixin
from .database import db
from datetime import datetime

class Rolesusers(db.Model):
    __tablename__ = 'rolesusers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id')) 

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    lastlogin = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(256), unique=True)
    roles = db.relationship('Role', secondary='rolesusers', backref=db.backref('users', lazy='dynamic'))

class StudentDetails(db.Model):
    __tablename__ = "studentdetails"
    sd_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    roll_no = db.Column(db.String, nullable=False, unique=True)
    current_status = db.Column(db.String, nullable=True)
    select_your_course = db.Column(db.String, nullable=True)
    commit_per_week = db.Column(db.Integer, nullable=True)
    budget_per_term = db.Column(db.Integer, nullable=True)
    CGPA = db.Column(db.Integer, nullable=True)
    interest = db.Column(db.String, nullable=True)
    about = db.Column(db.String(255), nullable=True)
    dob = db.Column(db.Date, default=datetime.utcnow().date())
    coursestatus = db.relationship("StudentCourseDetails", backref="cstudent")
    recommendation = db.relationship("Recommendation", backref="rstudent")

class Courses(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_name = db.Column(db.String(80), unique=True, nullable=False)
    level = db.Column(db.String(80), nullable=False)
    enrolled_this_term = db.Column(db.Integer, nullable=True)
    enrolled_so_far = db.Column(db.Integer, nullable=True)
    course_credit = db.Column(db.Integer, nullable=False)
    course_description = db.Column(db.String(255), nullable=False)
    teacher = db.Column(db.String(80), nullable=False)
    pre_req1 = db.Column(db.String(80), nullable=False)
    pre_req2 = db.Column(db.String(80), nullable=False)
    fees = db.Column(db.Integer, nullable=False)
    toughness = db.Column(db.Integer, nullable=True)
    avg_marks = db.Column(db.Integer, nullable=True)
    success_rate = db.Column(db.Integer, nullable=True)

class StudentCourseDetails(db.Model):
    __tablename__ = "usercourses"
    ucd_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_no = db.Column(db.String, db.ForeignKey("studentdetails.roll_no"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable=False)
    course_term = db.Column(db.Integer, nullable=False)
    course_status = db.Column(db.String, nullable=False)
    grade = db.Column(db.String, nullable=False)

class Feedback(db.Model):
    __tablename__ = "feedback"
    f_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_no = db.Column(db.String, db.ForeignKey("studentdetails.roll_no"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.course_id"), nullable=False)
    teacher = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assignment = db.Column(db.Integer, nullable=False)
    exams = db.Column(db.String, nullable=False)
    content = db.Column(db.Integer, nullable=False)
    toughness = db.Column(db.Integer, nullable=False)
    overall = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String, nullable=False)
    feedback = db.Column(db.String(255), nullable=False)
    student = db.relationship("StudentDetails", backref="feedback")

class StudentEnrollment(db.Model):
    __tablename__ = "studentenrollment"
    se_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term = db.Column(db.String, nullable=False)
    total_student_enrolled = db.Column(db.Integer, nullable=False)
    total_registered_student = db.Column(db.Integer, nullable=False)
    students_with_full_profile = db.Column(db.Integer, nullable=False)
    Average_score = db.Column(db.Integer, nullable=True)
    high_sub_rate = db.Column(db.Integer, nullable=True)


class Term(db.Model):
    __tablename__ = "term"
    t_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    term = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_student_enrolled = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(255), nullable=False)

class Recommendation(db.Model):
    __tablename__ = "recommendation"
    r_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_no = db.Column(db.String, db.ForeignKey("studentdetails.roll_no"), nullable=False)
    course_one = db.Column(db.String, db.ForeignKey("courses.course_name"), nullable=False)
    course_two = db.Column(db.String, db.ForeignKey("courses.course_name"), nullable=False)
    course_three = db.Column(db.String, db.ForeignKey("courses.course_name"), nullable=False)
    course_four = db.Column(db.String, db.ForeignKey("courses.course_name"), nullable=False)
    status = db.Column(db.String(255), nullable=False)
