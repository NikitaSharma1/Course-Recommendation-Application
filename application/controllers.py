from flask import render_template, jsonify,request
from flask import current_app as app
from flask_security import auth_required, current_user
from application.models import User,StudentDetails,Courses,Rolesusers,Role,Feedback, StudentCourseDetails, Recommendation
from application.validation import NotFoundError
from application.email import send_email_user
from jinja2 import Template
import random

from application.database import db
# ----------- APIs ----------------------------------------------------------------------#
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


def stats_to_json(course):
    return {
        "fees": course.fees,
        "toughness": course.toughness,
        "avg_marks": course.avg_marks,
        "success_rate": course.success_rate,
        "enrollments": course.enrolled_so_far,
        "teacher": course.teacher,
    }

def recommendation_to_json(recommendation):
    return {
        "r_id": recommendation.r_id,
        "roll_no": recommendation.roll_no,
        "course_one": recommendation.course_one,
        "course_two": recommendation.course_two,
        "course_three": recommendation.course_three,
        "course_four": recommendation.course_four,
        "status": recommendation.status
    }

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/satistics/<course>")
def satistics(course):
    course=Courses.query.filter_by(course_name=course).first()
    if course:
        return jsonify(stats_to_json(course))
    else:
        raise jsonify({"message":"Course not found"})


@auth_required('token')
@app.route("/usercourses")
def usercourses():
    user_id = current_user.id
    stud = StudentDetails.query.filter_by(user_id=user_id).first()
    if stud:
        if stud.interest is None:
            return jsonify([])
        interest = stud.interest.lower() 
        courses = Courses.query.filter_by(course_description=interest).all()
        
        if courses:
            cs=[course_to_json(i) for i in courses]
            return jsonify(cs)
        else:
            raise NotFoundError(status_code=404)
    else:
        courses = Courses.query.all()
        if courses:
            cs=[course_to_json(i) for i in courses]
            return jsonify(cs)
        else:
            raise NotFoundError(status_code=404)




@auth_required('token')
@app.route("/getroles")
def getroles():
    roles = current_user.roles
    if roles!=[]:
        role_name=roles[0].name
        return jsonify(role_name)
    else:
        return jsonify([{
        "id": 2,
        "name": "student",
        "description": "Student",
    }])


@auth_required('token')
@app.route("/getcourse/<course_name>")
def getcourses(course_name):
    course = Courses.query.filter_by(course_name=course_name).first()
    if course:
        return jsonify(course_to_json(course))
    else:
        raise NotFoundError(status_code=404)


@auth_required('token')
@app.route("/similarcourses/<course_name>")
def similarcourses(course_name):
    course = Courses.query.filter_by(course_name=course_name).first()
    course_description = course.course_description
    all_courses = Courses.query.filter_by(course_description=course_description).all()

    # Exclude the selected course
    courses = [course for course in all_courses if course.course_name != course_name]

    # Choose any 3 random courses from the table other than the course itself
    if len(courses) > 3:
        selected_courses = random.sample(courses, 3)
    else:
        selected_courses = courses

    return jsonify([course_to_json(course) for course in selected_courses])

@auth_required('token')
@app.route("/api/completedcourses", methods=["POST"])
def completedcourses():
    # get the roll_no from the current user 
    user_id = current_user.id
    stud = StudentDetails.query.filter_by(user_id=user_id).first()
    roll_no = stud.roll_no
    # print the post data 
    post_data = request.get_json()

    # post_data has course name as keys, use that to get the course_id from the Courses table
    for course_name in post_data:
        course_id = Courses.query.filter_by(course_name=course_name).first().course_id
        if post_data[course_name] == "":
            stud=StudentCourseDetails.query.filter_by(roll_no=roll_no, course_id=course_id).first()
            db.session.delete(stud)
            db.session.commit()
        
        
        # add the course_id, roll_no to the StudentCourseDetails table
        scd = StudentCourseDetails.query.filter_by(roll_no=roll_no, course_id=course_id).first()
        if scd:
            scd.course_id = course_id
            scd.roll_no = roll_no
            scd.completed = True
            scd.grade = post_data[course_name]
        else:
            if post_data[course_name] == "":
                continue
            scd = StudentCourseDetails(
                course_id=course_id,
                roll_no=roll_no,
                course_term="2023",
                course_status="Completed",
                grade=post_data[course_name],
            )
            db.session.add(scd)
        db.session.commit()
    return jsonify({"message": "Courses updated successfully"})

@auth_required('token')
@app.route("/api/completedcourses", methods=["GET"])
def getcompletedcourses(internal=False):
    user_id = current_user.id
    stud = StudentDetails.query.filter_by(user_id=user_id).first()
    roll_no = stud.roll_no
    scd = StudentCourseDetails.query.filter_by(roll_no=roll_no).all()
    if scd:
        courses = [Courses.query.filter_by(course_id=i.course_id).first() for i in scd]
        if internal:
            return courses
        return jsonify([course_to_json(course) for course in courses])
    else:
        return jsonify([])
    
@auth_required('token')
@app.route("/api/completecoursesgrades", methods=["GET"])
def getcompletedcoursesgrades():
    user_id = current_user.id
    stud = StudentDetails.query.filter_by(user_id=user_id).first()
    roll_no = stud.roll_no
    scd = StudentCourseDetails.query.filter_by(roll_no=roll_no).all()
    if scd:
        courses = [Courses.query.filter_by(course_id=i.course_id).first() for i in scd]
        grades=[i.grade for i in scd]
        return jsonify([course_to_json(course) for course in courses],grades)
    else:
        return jsonify([])


@auth_required('token')
@app.route("/api/totalcost", methods=["GET"])
def totalcost():
    user_id = current_user.id
    stud = StudentDetails.query.filter_by(user_id=user_id).first()
    roll_no = stud.roll_no
    scd = StudentCourseDetails.query.filter_by(roll_no=roll_no).all()
    if scd:
        courses = [Courses.query.filter_by(course_id=i.course_id).first() for i in scd]
        total_cost = sum([course.fees for course in courses])
        return jsonify({"total_cost": total_cost})
    else:
        return jsonify({"total_cost": 0})

@auth_required('token')
@app.route("/api/totalcredits", methods=["GET"])
def totalcredits():
    user_id = current_user.id
    stud = StudentDetails.query.filter_by(user_id=user_id).first()
    roll_no = stud.roll_no
    scd = StudentCourseDetails.query.filter_by(roll_no=roll_no).all()
    if scd:
        courses = [Courses.query.filter_by(course_id=i.course_id).first() for i in scd]
        total_credits = sum([course.course_credit for course in courses])
        return jsonify({"total_credits": total_credits})
    else:
        return jsonify({"total_credits": 0})

@auth_required('token')
@app.route("/api/savedrecommendation", methods=["GET"])
def savedrecommendation():
    user_id = current_user.id
    stud = StudentDetails.query.filter_by(user_id=user_id).first()
    roll_no = stud.roll_no
    rec = Recommendation.query.filter_by(roll_no=roll_no).all()
    if rec:
        # jsonify the rec row 
        return jsonify([recommendation_to_json(i) for i in rec])
    else:
        return jsonify([])
    

    




@app.route("/email", methods=["POST"])
def send_email():
    post_data = request.get_json()
    name = post_data["name"]
    email = post_data["email"]
    stud_message = post_data["message"]
    if name =="" or email== "":
        user=User.query.filter_by(id=current_user.id).first()
        name=user.username
        email=user.email
    if stud_message == "":
         return jsonify({"message": "Message is empty"})

    with open('templates/adminmail.html') as file_:
            template = Template(file_.read())
            message = template.render(name=name, query=stud_message, email=email)

    send_email_user(
            to="courserecommendation@gmail.com",
            sub="Student Query from Course Recommendation System",
            message=message
        )

    with open('templates/usermail.html') as file_:
            template = Template(file_.read())
            message = template.render(name=name, query=stud_message, email=email)

    send_email_user(
            to=email,
            sub="Message Received from Course Recommendation System",
            message=message
        )

    return jsonify({"message": "Message sent successfully"})


@app.route("/sendfeedback/<course_name>", methods=["POST"])
def send_feedback(course_name):
    course_id=Courses.query.filter_by(course_name=course_name).first().course_id
    feedback=Feedback.query.filter_by(course_id=course_id).all()
    if feedback ==[]:
         raise NotFoundError(status_code=404)

    with open('templates/feedbackmail.html') as file_:
            template = Template(file_.read())
            message = template.render(feedback=feedback)

    send_email_user(
            to="courserecommendation@gmail.com",
            sub="Student Feedbacks from Course Recommendation System",
            message=message
        )
    
    return jsonify({"message": "Message sent successfully"})



if __name__ == "__main__":
    app.run(debug=True)
        



