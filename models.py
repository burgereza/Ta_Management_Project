from database import db

class Professor(db.Model):
    __tablename__ = 'professors'
    personnel_code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(10), nullable=False)


class Student(db.Model):
    __tablename__ = 'students'
    student_number = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(10), nullable=False)


class BaseCourse(db.Model):
    __tablename__ = 'base_courses'
    code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(20), nullable=False)


class Course(db.Model):
    __tablename__ = 'courses'
    code = db.Column(db.String(10), primary_key=True)
    professor_id = db.Column(db.String(10), db.ForeignKey('professors.personnel_code'), primary_key=True)
    term = db.Column(db.String(5), primary_key=True)


class Request(db.Model):
    __tablename__ = 'requests'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(10), db.ForeignKey('students.student_number'), nullable=False)
    course_code = db.Column(db.String(10), nullable=False)
    professor_id = db.Column(db.String(10), nullable=False)
    term = db.Column(db.String(5), nullable=False)
    status = db.Column(db.String(10), default='pending')

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['course_code', 'professor_id', 'term'],
            ['courses.code', 'courses.professor_id', 'courses.term']
        ),
    )


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    ta_id = db.Column(db.String(10), db.ForeignKey('students.student_number'), nullable=False)
    course_code = db.Column(db.String(10), nullable=False)
    professor_id = db.Column(db.String(10), nullable=False)
    term = db.Column(db.String(5), nullable=False)
    reviewer_id = db.Column(db.String(10), db.ForeignKey('students.student_number'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['course_code', 'professor_id', 'term'],
            ['courses.code', 'courses.professor_id', 'courses.term']
        ),
    )