from database import db


class BaseCourse(db.Model):
    __tablename__ = 'base_courses'
    code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)



def get_all_base_courses():
    """دریافت همه دروس پایه"""
    return BaseCourse.query.all()


def get_base_course_by_code(course_code):
    """دریافت درس پایه با کد"""
    return BaseCourse.query.get(course_code)


def add_base_course(code, name):
    """افزودن درس پایه جدید"""
    existing = BaseCourse.query.get(code)
    if existing:
        return False
    base_course = BaseCourse(code=code, name=name)
    db.session.add(base_course)
    db.session.commit()
    return True