from database import db
from models.base_course import BaseCourse
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