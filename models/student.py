from database import db


class Student(db.Model):
    __tablename__ = 'students'
    student_number = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)


def get_student_by_student_number(student_number):
    return Student.query.get(student_number)


def update_student_password(student_number, old_password, new_password):
    student = Student.query.get(student_number)
    if student and student.password == old_password:
        student.password = new_password
        db.session.commit()
        return True
    return False


def add_student(student_number, name, password):
    existing = Student.query.get(student_number)
    if existing:
        return False
    student = Student(
        student_number=student_number,
        name=name,
        password=password
    )
    db.session.add(student)
    db.session.commit()
    return True


def get_all_students():
    return Student.query.all()