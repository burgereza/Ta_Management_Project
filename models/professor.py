from database import db


class Professor(db.Model):
    __tablename__ = 'professors'
    personnel_code = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)


def get_professor_by_personnel_code(personnel_code):
    return Professor.query.get(personnel_code)


def update_professor_password(personnel_code, old_password, new_password):
    professor = Professor.query.get(personnel_code)
    if professor and professor.password == old_password:
        professor.password = new_password
        db.session.commit()
        return True
    return False


def add_professor(personnel_code, name, password):
    existing = Professor.query.get(personnel_code)
    if existing:
        return False
    professor = Professor(
        personnel_code=personnel_code,
        name=name,
        password=password
    )
    db.session.add(professor)
    db.session.commit()
    return True


def get_all_professors():
    return Professor.query.all()