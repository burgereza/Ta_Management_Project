from database import db
from models.course_name import CourseName
from models.professor import Professor


class Course(db.Model):
    __tablename__ = 'courses'
    code = db.Column(db.String(20), primary_key=True)
    professor_id = db.Column(db.String(20), db.ForeignKey('professors.personnel_code'), primary_key=True)
    term = db.Column(db.String(20), primary_key=True)


def get_courses_by_professor(professor_id):
    courses = Course.query.filter_by(professor_id=professor_id).all()
    result = []
    for course in courses:
        course_name = CourseName.query.get(course.code)
        if course_name:
            result.append((course, course_name))
    return result


def get_course_by_code_and_term(course_code, professor_id, term):
    course = Course.query.filter_by(
        code=course_code,
        professor_id=professor_id,
        term=term
    ).first()
    if not course:
        return None
    course_name = CourseName.query.get(course.code)
    return (course, course_name)


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
        course_name = CourseName.query.get(course.code)
        if course_name:
            result.append((course, course_name))
    return result


def get_all_courses_with_professors():
    courses = Course.query.all()
    result = []
    for course in courses:
        course_name = CourseName.query.get(course.code)
        professor = Professor.query.get(course.professor_id)
        if course_name and professor:
            result.append((course, course_name, professor))
    return result