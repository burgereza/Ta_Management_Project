from database import db
from models.student import Student
from models.base_course import BaseCourse
from models.professor import Professor


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    ta_id = db.Column(db.String(20), db.ForeignKey('students.student_number'), nullable=False)
    course_code = db.Column(db.String(20), nullable=False)
    professor_id = db.Column(db.String(20), nullable=False)
    term = db.Column(db.String(20), nullable=False)
    reviewer_id = db.Column(db.String(20), db.ForeignKey('students.student_number'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)

    __table_args__ = (
        db.ForeignKeyConstraint(
            ['course_code', 'professor_id', 'term'],
            ['courses.code', 'courses.professor_id', 'courses.term']
        ),
    )


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