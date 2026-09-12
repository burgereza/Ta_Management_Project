from database import db
from models.student import Student
from models.course_name import CourseName
from models.professor import Professor


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), db.ForeignKey('students.student_number'), nullable=False)
    course_code = db.Column(db.String(20), nullable=False)
    professor_id = db.Column(db.String(20), nullable=False)
    term = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default='pending')

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['course_code', 'professor_id', 'term'],
            ['courses.code', 'courses.professor_id', 'courses.term']
        ),
    )


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


def get_requests_with_students_by_course(course_code, professor_id, term, status=None):
    requests = get_requests_by_course(course_code, professor_id, term, status)
    result = []
    for req in requests:
        student = Student.query.get(req.student_id)
        if student:
            result.append((req, student))
    return result


def get_student_requests_with_details(student_id):
    requests = Request.query.filter_by(student_id=student_id).order_by(Request.term.desc()).all()
    result = []
    for req in requests:
        course_name = CourseName.query.get(req.course_code)
        professor = Professor.query.get(req.professor_id)
        if course_name and professor:
            result.append((req, course_name, professor))
    return result


def get_courses_with_accepted_tas():
    from models.course import Course
    all_courses = Course.query.all()
    result = []
    for course in all_courses:
        accepted = Request.query.filter_by(
            course_code=course.code,
            professor_id=course.professor_id,
            term=course.term,
            status='accepted'
        ).all()
        if accepted:
            course_name = CourseName.query.get(course.code)
            professor = Professor.query.get(course.professor_id)
            if course_name and professor:
                result.append((course, course_name, professor))
    return result