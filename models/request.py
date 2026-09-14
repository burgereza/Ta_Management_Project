from database import db
from models.student import Student
from models.course_name import CourseName
from models.professor import Professor
from models.course import Course
from models.student import Student

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


def get_course_requests(course_code, professor_id, term, status=None):
    query = Request.query.filter_by(course_code=course_code, professor_id=professor_id, term=term)
    if status:
        query = query.filter_by(status=status)
    return query.all()


def get_request_by_student_and_course(student_id, course_code, professor_id, term):
    return Request.query.filter_by(student_id=student_id, course_code=course_code, professor_id=professor_id, term=term).first()


def add_new_request(student_id, course_code, professor_id, term, status='pending'):
    req = Request(student_id=student_id, course_code=course_code, professor_id=professor_id, term=term, status=status)
    db.session.add(req)
    db.session.commit()
    return req


def change_request_status(request_id, new_status):
    req = Request.query.get(request_id)
    if req:
        req.status = new_status
        db.session.commit()
        return True
    return False


def get_request_by_id(request_id):
    return Request.query.get(request_id)
