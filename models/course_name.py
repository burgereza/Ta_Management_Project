from database import db


class CourseName(db.Model):
    __tablename__ = 'course_name'
    code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)



def get_all_course_names():
    return CourseName.query.all()


def get_course_name_by_code(course_code):
    return CourseName.query.get(course_code)


def add_course_name(code, name):
    existing = CourseName.query.get(code)
    if existing:
        return False
    course_name = CourseName(code=code, name=name)
    db.session.add(course_name)
    db.session.commit()
    return True