from database import db
from models.course_name import CourseName
from models.professor import Professor


class Course(db.Model):
    __tablename__ = 'courses'
    code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    professor_id = db.Column(db.String(20), db.ForeignKey('professors.personnel_code'), primary_key=True)
    term = db.Column(db.String(20), primary_key=True)


def get_all_professor_courses(professor_id):
    return Course.query.filter_by(professor_id=professor_id).all()


def get_course(course_code, professor_id, term):
    return Course.query.filter_by(code=course_code, professor_id=professor_id, term=term).first()


def add_professor_course(course_code, course_name, professor_id, term):
    existing = Course.query.filter_by(code=course_code, professor_id=professor_id, term=term).first()
    if existing:
        return None
    course = Course(code=course_code, name=course_name, professor_id=professor_id, term=term)
    db.session.add(course)
    db.session.commit()
    return course


def get_all_courses():
    return Course.query.all()
