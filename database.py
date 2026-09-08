from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from models import Professor, Student, BaseCourse, Course, Request, Review



def get_professor_by_personnel_code(personnel_code):
    return Professor.query.get(personnel_code)


def update_professor_password(personnel_code, new_password):
    professor = Professor.query.get(personnel_code)
    if professor:
        professor.password = new_password
        db.session.commit()
        return True
    return False



def get_student_by_student_number(student_number):
    return Student.query.get(student_number)


def update_student_password(student_number, new_password):
    student = Student.query.get(student_number)
    if student:
        student.password = new_password
        db.session.commit()
        return True
    return False



def get_all_base_courses():
    return BaseCourse.query.all()


def get_base_course_by_code(course_code):
    return BaseCourse.query.get(course_code)



def get_courses_by_professor(professor_id):
    courses = Course.query.filter_by(professor_id=professor_id).all()
    result = []
    for course in courses:
        base_course = BaseCourse.query.get(course.code)
        if base_course:
            result.append((course, base_course))
    return result


def get_course_by_code_and_term(course_code, professor_id, term):
    course = Course.query.filter_by(
        code=course_code,
        professor_id=professor_id,
        term=term
    ).first()
    if not course:
        return None
    base_course = BaseCourse.query.get(course.code)
    return (course, base_course)


def add_course_for_professor(course_code, professor_id, term):
    existing = Course.query.filter_by(
        code=course_code,
        professor_id=professor_id,
        term=term
    ).first()
    if existing:
        return None
    course = Course(code=course_code, professor_id=professor_id, term=term)
    db.session.add(course)
    db.session.commit()
    return course


def delete_course(course_code, professor_id, term):
    course = Course.query.filter_by(
        code=course_code,
        professor_id=professor_id,
        term=term
    ).first()
    if course:
        db.session.delete(course)
        db.session.commit()
        return True
    return False


def get_all_courses():
    courses = Course.query.all()
    result = []
    for course in courses:
        base_course = BaseCourse.query.get(course.code)
        if base_course:
            result.append((course, base_course))
    return result


def get_all_courses_with_professors():
    courses = Course.query.all()
    result = []
    for course in courses:
        base_course = BaseCourse.query.get(course.code)
        professor = Professor.query.get(course.professor_id)
        if base_course and professor:
            result.append((course, base_course, professor))
    return result


def get_courses_with_accepted_tas():
    all_courses = Course.query.all()
    result = []
    
    for course in all_courses:
        accepted_requests = Request.query.filter_by(
            course_code=course.code,
            professor_id=course.professor_id,
            term=course.term,
            status='accepted'
        ).all()
        
        if accepted_requests:
            base_course = BaseCourse.query.get(course.code)
            professor = Professor.query.get(course.professor_id)
            if base_course and professor:
                result.append((course, base_course, professor))
    
    return result



def get_requests_by_course(course_code, professor_id, term, status=None):
    query = Request.query.filter_by(
        course_code=course_code,
        professor_id=professor_id,
        term=term
    )
    if status:
        query = query.filter_by(status=status)
    return query.all()


def get_request_by_student_and_course(student_id, course_code, professor_id, term):
    return Request.query.filter_by(
        student_id=student_id,
        course_code=course_code,
        professor_id=professor_id,
        term=term
    ).first()


def add_new_request(student_id, course_code, professor_id, term, status='pending'):
    req = Request(
        student_id=student_id,
        course_code=course_code,
        professor_id=professor_id,
        term=term,
        status=status
    )
    db.session.add(req)
    db.session.commit()
    return req


def update_request_status(request_id, new_status):
    req = Request.query.get(request_id)
    if req:
        req.status = new_status
        db.session.commit()
        return True
    return False


def get_request_by_id(request_id):
    return Request.query.get(request_id)


def get_accepted_requests_for_course(course_code, professor_id, term):
    return Request.query.filter_by(
        course_code=course_code,
        professor_id=professor_id,
        term=term,
        status='accepted'
    ).all()


def get_requests_by_student(student_id):
    return Request.query.filter_by(student_id=student_id).all()


def get_requests_with_students_by_course(course_code, professor_id, term, status=None):
    requests = get_requests_by_course(course_code, professor_id, term, status)
    result = []
    for req in requests:
        student = Student.query.get(req.student_id)
        if student:
            result.append((req, student))
    return result



def add_new_review(ta_id, course_code, professor_id, term, reviewer_id, rating, comment):
    review = Review(
        ta_id=ta_id,
        course_code=course_code,
        professor_id=professor_id,
        term=term,
        reviewer_id=reviewer_id,
        rating=rating,
        comment=comment
    )
    db.session.add(review)
    db.session.commit()
    return review


def check_student_review_for_course(ta_id, course_code, professor_id, term, reviewer_id):
    return Review.query.filter_by(
        ta_id=ta_id,
        course_code=course_code,
        professor_id=professor_id,
        term=term,
        reviewer_id=reviewer_id
    ).first()


def get_reviews_by_ta(ta_id):
    return Review.query.filter_by(ta_id=ta_id).all()


def get_reviews_with_reviewers(ta_id):
    reviews = Review.query.filter_by(ta_id=ta_id).all()
    result = []
    for review in reviews:
        reviewer = Student.query.get(review.reviewer_id)
        if reviewer:
            result.append((review, reviewer))
    return result


def get_reviews_with_course_and_professor(ta_id):
    reviews = Review.query.filter_by(ta_id=ta_id).all()
    result = []
    
    for review in reviews:
        base_course = BaseCourse.query.get(review.course_code)
        professor = Professor.query.get(review.professor_id)
        reviewer = Student.query.get(review.reviewer_id)
        
        if base_course and professor and reviewer:
            result.append((review, base_course, professor, reviewer))
    
    return result



def get_student_requests_with_details(student_id):
    requests = Request.query.filter_by(student_id=student_id).order_by(Request.term.desc()).all()
    result = []
    
    for req in requests:
        base_course = BaseCourse.query.get(req.course_code)
        professor = Professor.query.get(req.professor_id)
        if base_course and professor:
            result.append((req, base_course, professor))
    
    return result