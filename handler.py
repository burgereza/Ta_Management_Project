from models.request import Request
from models.course import Course
from models.professor import Professor
import models
from models.student import Student



def get_course_tas(course_code, professor_id, term):
    accepted_requests = Request.query.filter_by(course_code=course_code, professor_id=professor_id, term=term, status='accepted').all()
    tas = []
    for req in accepted_requests:
        student = Student.query.get(req.student_id)
        if student:
            tas.append(student)
    return tas



def get_requests_students_by_course(course_code, professor_id, term, status=None):
    requests = models.request.get_course_requests(course_code, professor_id, term, status)
    result = []
    for request in requests:
        student = Student.query.get(request.student_id)
        if student:
            result.append((request, student))
    return result



def get_student_requests(student_id):
    requests = Request.query.filter_by(student_id=student_id).order_by(Request.term.desc()).all()
    result = []
    for req in requests:
        course = Course.query.filter_by(
            code=req.course_code,
            professor_id=req.professor_id,
            term=req.term
        ).first()
        professor = Professor.query.get(req.professor_id)
        if course and professor:
            result.append({'course_name': course.name, 'professor_name': professor.name, 'term': req.term, 'status': req.status})
    return result




def get_courses_with_status_for_student(student_id): 
    all_courses = Course.query.all()
    result = []
    for course in all_courses:
        professor = Professor.query.get(course.professor_id)
        req = Request.query.filter_by(student_id=student_id, course_code=course.code, professor_id=course.professor_id, term=course.term).first()
        
        if req:
            status = req.status
        else:
            status = None
        
        if professor:
            result.append({'course': course, 'professor': professor, 'status': status})
    return result



def get_courses_for_review(student_id):
    all_courses = Course.query.all()
    result = []
    for course in all_courses:
        accepted = Request.query.filter_by(course_code=course.code, professor_id=course.professor_id, term=course.term, status='accepted').all()
        
        student_is_ta = False
        for req in accepted:
            if req.student_id == student_id:
                student_is_ta = True
                break
        
        if not student_is_ta:
            professor = Professor.query.get(course.professor_id)
            if professor:
                result.append({'course': course, 'professor': professor})
    return result