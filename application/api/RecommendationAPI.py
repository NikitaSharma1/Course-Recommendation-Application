from flask_restful import Resource
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from application.validation import NotGivenError, NotFoundError
from application.models import Recommendation, StudentDetails, Courses, StudentCourseDetails
from application.database import db
from flask import jsonify
from flask_security import current_user, auth_required,roles_required
from sqlalchemy import and_
from itertools import permutations,combinations_with_replacement
from itertools import product
import random


recommendation_fields = {
    "r_id": fields.Integer,
    "roll_no": fields.String,
    "course_one": fields.String,
    "course_two": fields.String,
    "course_three": fields.String,
    "course_four": fields.String,
    "status": fields.String,
}

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


recommendation_parse = reqparse.RequestParser()
recommendation_parse.add_argument("r_id")
recommendation_parse.add_argument("roll_no")
recommendation_parse.add_argument("course_one")
recommendation_parse.add_argument("course_two")
recommendation_parse.add_argument("course_three")
recommendation_parse.add_argument("course_four")
recommendation_parse.add_argument("status")

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

import random

def get_combination_2(easy_courses, medium_courses, hard_courses):
    combo = [(1, 1, 0), (1, 0, 1), (0, 1, 1), (2, 0, 0), (0, 2, 0), (0, 0, 2)]
    for easy_count, medium_count, hard_count in combo:
        combination = []

        for _ in range(easy_count):
            if easy_courses:
                course = random.choice(easy_courses)
                combination.append(course_to_json(course))

        for _ in range(medium_count):
            if medium_courses:
                course = random.choice(medium_courses)
                combination.append(course_to_json(course))

        for _ in range(hard_count):
            if hard_courses:
                course = random.choice(hard_courses)
                combination.append(course_to_json(course))

        if len(set(course["course_id"] for course in combination)) == len(combination):
            return combination

def get_combination_3(easy_courses, medium_courses, hard_courses):
    combo = [(1, 1, 1), (2, 1, 0), (2, 0, 1), (1, 2, 0), (1, 0, 2), (0, 2, 1), (0, 1, 2), (3, 0, 0), (0, 3, 0), (0, 0, 3)]
    for easy_count, medium_count, hard_count in combo:
        combination = []

        for _ in range(easy_count):
            if easy_courses:
                course = random.choice(easy_courses)
                combination.append(course_to_json(course))

        for _ in range(medium_count):
            if medium_courses:
                course = random.choice(medium_courses)
                combination.append(course_to_json(course))

        for _ in range(hard_count):
            if hard_courses:
                course = random.choice(hard_courses)
                combination.append(course_to_json(course))

        if len(set(course["course_id"] for course in combination)) == len(combination):
            return combination

def get_combination_4(easy_courses, medium_courses, hard_courses):
    combo = [(0, 1, 3), (0, 2, 2), (0, 3, 1), (1, 0, 3), (1, 1, 2), (1, 2, 1), (1, 3, 0), (2, 0, 2), (2, 1, 1), (2, 2, 0), (3, 0, 1), (3, 1, 0), (0, 0, 4), (0, 4, 0), (4, 0, 0)]
    for easy_count, medium_count, hard_count in combo:
        combination = []

        for _ in range(easy_count):
            if easy_courses:
                course = random.choice(easy_courses)
                combination.append(course_to_json(course))

        for _ in range(medium_count):
            if medium_courses:
                course = random.choice(medium_courses)
                combination.append(course_to_json(course))

        for _ in range(hard_count):
            if hard_courses:
                course = random.choice(hard_courses)
                combination.append(course_to_json(course))

        if len(set(course["course_id"] for course in combination)) == len(combination):
            return combination

def recommend_courses_based_on_toughness(student, count):
    stud = StudentDetails.query.filter_by(user_id=current_user.id).first()
    if stud:
        interest = stud.interest.lower()
    courses = Courses.query.filter_by(course_description=interest).all()
    stu_courses = StudentCourseDetails.query.filter_by(roll_no=student.roll_no).all()
    courses_left = [c for c in courses if all(sc.course_id != c.course_id or sc.grade == "U" for sc in stu_courses)]
    
    prereq_courses_name = set()
    easy_courses = []
    medium_courses = []
    hard_courses = []

    courses_left_names = {c.course_name for c in courses_left}

    for cl in courses_left:
        if cl.pre_req1 in courses_left_names:
            prereq_courses_name.add(cl.pre_req1)
        if cl.pre_req2 in courses_left_names:
            prereq_courses_name.add(cl.pre_req2)
        if cl.toughness > 7:
            hard_courses.append(cl)
        elif 5 < cl.toughness <= 7:
            medium_courses.append(cl)
        elif cl.toughness <= 5:
            easy_courses.append(cl)
    
    hard_courses = sorted(hard_courses, key=lambda x: x.toughness, reverse=True)
    medium_courses = sorted(medium_courses, key=lambda x: x.toughness, reverse=True)
    easy_courses = sorted(easy_courses, key=lambda x: x.toughness, reverse=True)

    prereq_courses = [course_to_json(course) for course in courses_left if course.course_name in prereq_courses_name]
    p1=[course_to_json(course) for course in courses_left if course.course_name in prereq_courses_name]
    recommended_courses = [p1]
    if len(prereq_courses) < count and len(hard_courses) > 0:
        for i in hard_courses:
            if course_to_json(i) not in prereq_courses:
                prereq_courses.append(course_to_json(i))
                if len(prereq_courses) == count:
                    break

    if len(prereq_courses) < count and len(easy_courses) > 0:
        for i in easy_courses:
            if course_to_json(i) not in prereq_courses:
                prereq_courses.append(course_to_json(i))
                if len(prereq_courses) == count:
                    break
    if len(prereq_courses) < count and len(medium_courses) > 0:
        for i in medium_courses:
            if course_to_json(i) not in prereq_courses:
                prereq_courses.append(course_to_json(i))
                if len(prereq_courses) == count:
                    break

    recommended_courses.append(prereq_courses)

    # Helper function to get combinations based on count
    def get_combinations(easy, medium, hard, combo_func, num_combinations):
        combinations = []
        for _ in range(num_combinations):
            combination = combo_func(easy, medium, hard)
            if combination:
                combinations.append(combination)
        return combinations

    # Add more combinations if the length is less than 6
    while len(recommended_courses) < 7:
        if count == 2:
            combinations = get_combinations(easy_courses, medium_courses, hard_courses, get_combination_2, 1)
            recommended_courses.extend(combinations)
        elif count == 3:
            combinations = get_combinations(easy_courses, medium_courses, hard_courses, get_combination_3, 1)
            recommended_courses.extend(combinations)
        elif count == 4:
            combinations = get_combinations(easy_courses, medium_courses, hard_courses, get_combination_4, 1)
            recommended_courses.extend(combinations)

    for i in recommended_courses[1:]:
        random.shuffle(i)
        if len(i) < count:
            recommended_courses.remove(i)

    return recommended_courses  # Ensure the final list has at most 6 combinations

def is_true_recommendation(roll_no,course_one,course_two,course_three,course_four):
    rc = Recommendation.query.filter_by(roll_no=roll_no).all()
    flag=False
    if rc!=[]:
        for i in rc:
            list1=[i.course_one,i.course_two,i.course_three,i.course_four]
            list2=[course_one,course_two,course_three,course_four]
            if course_four is None:
                list2=[course_one,course_two,course_three,"Nil"]
            if course_four is None and course_three is None:
                list2=[course_one,course_two,"Nil","Nil"]
            if set(list1) == set(list2):
                flag=True
    return flag

def recommend_courses(student):
            recommended_courses = []
            
            # Check if budget, commit_per_week, and CGPA meet the conditions
            if student.budget_per_term == 40000 and student.commit_per_week == 40 and student.CGPA >= 8:
                # Recommend up to 4 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 4)+recommend_courses_based_on_toughness(student, 3)+recommend_courses_based_on_toughness(student, 2)
                 
            if student.budget_per_term == 30000 and student.commit_per_week == 30 and student.CGPA >= 8:
                # Recommend up to 3 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 3)+recommend_courses_based_on_toughness(student, 2)
                
            if student.budget_per_term == 20000 and student.commit_per_week == 20 and student.CGPA >= 8:
                # Recommend up to 2 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 2)

            if student.budget_per_term == 40000 and student.commit_per_week == 40 and 6 <= student.CGPA < 8:
                # Recommend up to 3 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 3)+recommend_courses_based_on_toughness(student, 2)
            
            if student.budget_per_term == 30000 and student.commit_per_week == 30 and 6 <= student.CGPA < 8:
                # Recommend up to 2 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 2)
            
           
            
            if student.budget_per_term == 40000 and student.commit_per_week == 40 and student.CGPA < 6:
                # Recommend up to 2 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 2)
            
            if student.budget_per_term == 40000 and student.commit_per_week == 30:
                # Recommend up to 4&3 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 4) + recommend_courses_based_on_toughness(student, 3)+recommend_courses_based_on_toughness(student, 2)
            
            if student.budget_per_term == 30000 and student.commit_per_week == 40:
                # Recommend up to 3&4 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 3) + recommend_courses_based_on_toughness(student, 4)

            if student.budget_per_term == 30000 and student.commit_per_week == 20:
                # Recommend up to 2&3 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 2) + recommend_courses_based_on_toughness(student, 3)

            if student.budget_per_term == 20000 and student.commit_per_week == 30:
                # Recommend up to 2&3 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 2) + recommend_courses_based_on_toughness(student, 3)

            if student.budget_per_term == 20000 and student.commit_per_week == 20:
                # Recommend up to 2 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 2)

            if student.budget_per_term == 20000 and student.commit_per_week == 40:
                # Recommend up to 3 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 3)+recommend_courses_based_on_toughness(student, 2)

            if student.budget_per_term == 40000 and student.commit_per_week == 20:
                # Recommend up to 2 courses
                recommended_courses = recommend_courses_based_on_toughness(student, 2)+recommend_courses_based_on_toughness(student, 3)
            

            return recommended_courses




class RecommendationAPI(Resource):
    @auth_required('token')
    @roles_required('student')
    def get(self):
        
        id=current_user.id
        # Assuming you have the student details retrieved from the database
        stud= StudentDetails.query.filter_by(user_id=id).first()  # Fetch the student by their ID
        recommended_courses = recommend_courses(stud)
        
        return jsonify(recommended_courses)

    @auth_required('token')
    @roles_required('student')
    def post(self):
        args = recommendation_parse.parse_args()
        stud=StudentDetails.query.filter_by(user_id=current_user.id).first()
        roll_no = stud.roll_no
        course_one = args.get("course_one")
        course_two = args.get("course_two")
        course_three = args.get("course_three")
        course_four = args.get("course_four")
        status = args.get("status")

        red=Recommendation.query.filter_by(roll_no=roll_no).all()
        if len(red)==3:
            reco_del=Recommendation.query.filter_by(roll_no=roll_no).first()
            db.session.delete(reco_del)
            db.session.commit()
        
        if course_four is None:
                status = "saved"
                course_four="Nil"
        
        if course_three is None:
            status = "saved"
            course_four="Nil"
            course_three="Nil"
        
        if status is None:
            status = "saved"

        if roll_no is None:
            raise NotGivenError(
                status_code=400,
                error_code="R001",
                error_message="roll_no is required",
            )
        if course_one is None:
            raise NotGivenError(
                status_code=400,
                error_code="R002",
                error_message="course_one is required",
            )
        
        if course_two is None:
            raise NotGivenError(
                status_code=400,
                error_code="R003",
                error_message="course_two is required",
            )
        
        if course_three is None:
            raise NotGivenError(
                status_code=400,
                error_code="R004",
                error_message="course_three is required",
            )
        
        if course_four is None:
            raise NotGivenError(
                status_code=400,
                error_code="R005",
                error_message="course_four is required",
            )
        
        if status is None:
            raise NotGivenError(
                status_code=400,
                error_code="R006",
                error_message="status is required",
            )
        flag=is_true_recommendation(roll_no,course_one,course_two,course_three,course_four)
        if flag:
            raise NotGivenError(
                status_code=400,
                error_code="R007",
                error_message="recommendation already exist",
            )
                
        else:
            rc = Recommendation(
                roll_no=roll_no,
                course_one=course_one,
                course_two=course_two,
                course_three=course_three,
                course_four=course_four,
                status=status,
            )
            db.session.add(rc)
            db.session.commit()
            return recommendation_to_json(rc),201
        
    # @auth_required('token')
    # @roles_required('student')
    def delete(self, recommendation_id):
        rc = Recommendation.query.filter_by(r_id=recommendation_id).first()
        if rc:
            db.session.delete(rc)
            db.session.commit()
            return {"message":"sucessfully deleted"}, 200

        else:
            raise NotFoundError(status_code=404)
        
    # @marshal_with(recommendation_fields)
    # @auth_required('token')
    # @roles_required('student')
    def put(self, recommendation_id):
        args = recommendation_parse.parse_args()
        roll_no = args.get("roll_no")
        course_one = args.get("course_one")
        course_two = args.get("course_two")
        course_three = args.get("course_three")
        course_four = args.get("course_four")
        status = args.get("status")

        if roll_no is None:
            raise NotGivenError(
                status_code=400,
                error_code="R001",
                error_message="roll_no is required",
            )
        if course_one is None:
            raise NotGivenError(
                status_code=400,
                error_code="R002",
                error_message="course_one is required",
            )
        
        if course_two is None:
            raise NotGivenError(
                status_code=400,
                error_code="R003",
                error_message="course_two is required",
            )
        
        if course_three is None:
            raise NotGivenError(
                status_code=400,
                error_code="R004",
                error_message="course_three is required",
            )
        
        if course_four is None:
            raise NotGivenError(
                status_code=400,
                error_code="R005",
                error_message="course_four is required",
            )
        
        if status is None:
            raise NotGivenError(
                status_code=400,
                error_code="R006",
                error_message="status is required",
            )
        
        rc = Recommendation.query.filter_by(r_id=recommendation_id).first()
        if rc:
            rc.roll_no = roll_no
            rc.course_one = course_one
            rc.course_two = course_two
            rc.course_three = course_three
            rc.course_four = course_four
            rc.status = status
            db.session.commit()
            return recommendation_to_json(rc), 200

        else:
            raise NotFoundError(status_code=404)