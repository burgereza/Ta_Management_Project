from flask import Flask, render_template, redirect, url_for, session, request, flash
from database import db
import database 

app = Flask(__name__)
app.secret_key = '1111'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1000@localhost/TaManagementDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
#db.create_all()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login_professor', methods=['GET', 'POST'])
def login_professor():
    if request.method == 'POST':
        personnel_code = request.form['personnel_code']
        password = request.form['password']
        
        professor = database.get_professor_by_personnel_code(personnel_code)
        if professor.password == password:
            session['user_id'] = personnel_code
            session['user_name'] = professor.name
            return redirect(url_for('professor_dashboard'))
        else:
            flash('کد پرسنلی یا رمز عبور اشتباه است')
    
    return render_template('login_professor.html')


@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        student_number = request.form['student_number']
        password = request.form['password']
        
        student = database.get_student_by_student_number(student_number)
        if student.password == password:
            session['user_id'] = student_number
            session['user_name'] = student.name
            return redirect(url_for('student_dashboard'))
        else:
            flash('شماره دانشجویی یا رمز عبور اشتباه است')
    
    return render_template('login_student.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



@app.route('/professor_dashboard')
def professor_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    professor_id = session['user_id']
    section = request.args.get('section', 'courses')

    if section == 'profile':
        return render_template('professor_dashboard.html', section='profile')

    if section == 'add_course':
        base_courses = database.get_all_base_courses()
        return render_template('professor_dashboard.html', 
                             section='add_course', 
                             base_courses=base_courses)

    courses_with_base = database.get_courses_by_professor(professor_id)
    courses = []
    for course, base_course in courses_with_base:
        courses.append({
            'course': course,
            'base_course': base_course
        })
    return render_template('professor_dashboard.html', section='courses', courses=courses)


@app.route('/add_course', methods=['POST'])
def add_course_route():
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    professor_id = session['user_id']

    course_code = request.form['course_code']
    term = request.form['term']
    
    if database.get_course_by_code_and_term(course_code, professor_id, term):
        flash('درس تکراری است')
        return redirect(url_for('professor_dashboard'))
    
    database.add_course_for_professor(course_code, professor_id, term)
    flash('درس با موفقیت اضافه شد')
    
    return redirect(url_for('professor_dashboard'))


@app.route('/delete_course')
def delete_course_route():
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    professor_id = session['user_id']
    
    course_code = request.args.get('course_code')
    term = request.args.get('term')

    database.delete_course(course_code, professor_id, term)
    flash('درس با موفقیت حذف شد')
    
    return redirect(url_for('professor_dashboard'))


@app.route('/professor_course')
def professor_course():
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    professor_id = session['user_id']
   

    course_code = request.args.get('course_code')
    term = request.args.get('term')
    
    course, base_course = database.get_course_by_code_and_term(course_code, professor_id, term)

    pending = database.get_requests_with_students_by_course(course_code, professor_id, term, 'pending')
    accepted = database.get_requests_with_students_by_course(course_code, professor_id, term, 'accepted')
    
    return render_template('professor_course.html', 
                         course=course,
                         base_course=base_course,
                         pending=pending, 
                         accepted=accepted)


@app.route('/accept_request/<int:request_id>')
def accept_request_route(request_id):
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    professor_id = session['user_id']

    req = database.get_request_by_id(request_id)
    
    database.update_request_status(request_id, 'accepted')
    flash('درخواست با موفقیت پذیرفته شد')
        
    
    if req:
        return redirect(url_for('professor_course', 
                              course_code=req.course_code, 
                              term=req.term))
    else:
        return redirect(url_for('professor_dashboard'))


@app.route('/student_ta_history/<student_id>')
def student_ta_history(student_id):
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    professor_id = session['user_id']

    student = database.get_student_by_student_number(student_id)
    reviews_data = database.get_reviews_with_course_and_professor(student_id)
    
    reviews = []
    for review, base_course, professor_obj, reviewer in reviews_data:
        reviews.append({
            'course_name': base_course.name,
            'professor_name': professor_obj.name,
            'term': review.term,
            'rating': review.rating,
            'comment': review.comment,
            'reviewer_name': reviewer.name
        })

    requests_data = database.get_student_requests_with_details(student_id)
    requests = []
    for req, base_course, professor_obj in requests_data:
        requests.append({
            'course_name': base_course.name,
            'professor_name': professor_obj.name,
            'term': req.term,
            'status': req.status
        })
    
    return render_template('student_ta_history.html', 
                         student=student,
                         reviews=reviews,
                         requests=requests)


@app.route('/change_professor_password', methods=['POST'])
def change_professor_password_route():
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    professor_id = session['user_id']

    new_password = request.form['new_password']
    
    database.update_professor_password(professor_id, new_password)
    flash('رمز عبور با موفقیت تغییر کرد')
    
    return redirect(url_for('professor_dashboard', section='profile'))



@app.route('/student_dashboard')
def student_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_student'))

    student_id = session['user_id']
    section = request.args.get('section', 'courses')

    if section == 'profile':
        return render_template('student_dashboard.html', section='profile')

    if section == 'review':
        courses_with_accepted_tas = database.get_courses_with_accepted_tas()
        courses = []
        for course, base_course, professor in courses_with_accepted_tas:
            courses.append({
                'course': course,
                'base_course': base_course,
                'professor': professor
            })
        return render_template('student_dashboard.html', section='review', courses=courses)

    all_courses_with_professors = database.get_all_courses_with_professors()
    courses_with_status = []
    
    for course, base_course, professor in all_courses_with_professors:
        req = database.get_request_by_student_and_course(
            student_id, 
            course.code, 
            course.professor_id, 
            course.term
        )
        status = req.status if req else None
        
        courses_with_status.append({
            'course': course,
            'base_course': base_course,
            'professor': professor,
            'status': status
        })
    
    return render_template('student_dashboard.html', section='courses', courses=courses_with_status)


@app.route('/request_ta')
def request_ta_route():
    if 'user_id' not in session:
        return redirect(url_for('login_student'))

    student_id = session['user_id']

    course_code = request.args.get('course_code')
    professor_id = request.args.get('professor_id')
    term = request.args.get('term')

    if  database.get_request_by_student_and_course(student_id, course_code, professor_id, term):
        flash('شما قبلاً برای این درس درخواست داده‌اید')
        return redirect(url_for('student_dashboard'))
    
    database.add_new_request(student_id, course_code, professor_id, term, 'pending')
    flash('درخواست شما با موفقیت ثبت شد')

    return redirect(url_for('student_dashboard'))


@app.route('/review_course')
def review_course():
    if 'user_id' not in session:
        return redirect(url_for('login_student'))

    student_id = session['user_id']

    course_code = request.args.get('course_code')
    professor_id = request.args.get('professor_id')
    term = request.args.get('term')
    
    course, base_course = database.get_course_by_code_and_term(course_code, professor_id, term)

    accepted_requests = database.get_accepted_requests_for_course(course_code, professor_id, term)
    tas = []
    for req in accepted_requests:
        student_obj = database.get_student_by_student_number(req.student_id)
        if student_obj:
            tas.append(student_obj)
    
    return render_template('review.html', course=course, base_course=base_course, tas=tas)


@app.route('/add_review', methods=['POST'])
def add_review_route():
    if 'user_id' not in session:
        return redirect(url_for('login_student'))

    reviewer_id = session['user_id']

    ta_id = request.form['ta_id']
    course_code = request.form['course_code']
    professor_id = request.form['professor_id']
    term = request.form['term']
    rating = int(request.form['rating'])
    comment = request.form['comment']

    existing_review = database.check_student_review_for_course(
        ta_id, course_code, professor_id, term, reviewer_id
    )
    
    if existing_review:
        flash('شما قبلاً برای این دستیار در این درس نظر ثبت کرده‌اید')
        return redirect(url_for('review_course', course_code=course_code, professor_id=professor_id, term=term))

    database.add_new_review(ta_id, course_code, professor_id, term, reviewer_id, rating, comment)
    flash('نظر شما با موفقیت ثبت شد')
    
    return redirect(url_for('student_dashboard', section='review'))


@app.route('/change_student_password', methods=['POST'])
def change_student_password_route():
    if 'user_id' not in session:
        return redirect(url_for('login_student'))

    student_id = session['user_id']
    new_password = request.form['new_password']
    
    database.update_student_password(student_id, new_password)
    flash('رمز عبور با موفقیت تغییر کرد')
    
    return redirect(url_for('student_dashboard', section='profile'))



# Admin:

@app.route('/admin1234', methods=['GET', 'POST'])
def admin_panel():
  
    if request.method == 'POST' and 'add_professor' in request.form:
        personnel_code = request.form['personnel_code']
        name = request.form['professor_name']
        password = request.form['professor_password']
        
        if database.get_professor_by_personnel_code(personnel_code):
            flash('کد پرسنلی تکراری است')
        else:
            new_professor = database.Professor(
                personnel_code=personnel_code,
                name=name,
                password=password
            )
            db.session.add(new_professor)
            db.session.commit()
            flash(' با موفقیت اضافه شد')
    

    if request.method == 'POST' and 'add_student' in request.form:
        student_number = request.form['student_number']
        name = request.form['student_name']
        password = request.form['student_password']
        
        if database.get_student_by_student_number(student_number):
            flash('شماره دانشجویی تکراری است')
        else:
            new_student = database.Student(
                student_number=student_number,
                name=name,
                password=password
            )
            db.session.add(new_student)
            db.session.commit()
            flash(' با موفقیت اضافه شد')
    
    if request.method == 'POST' and 'add_base_course' in request.form:
        code = request.form['course_code']
        name = request.form['course_name']
        
        if database.get_base_course_by_code(code):
            flash('کد درس تکراری است')
        else:
            new_course = database.BaseCourse(
                code=code,
                name=name
            )
            db.session.add(new_course)
            db.session.commit()
            flash('با موفقیت اضافه شد')
    
    return render_template('admin_panel.html')



if __name__ == '__main__':
    app.run(debug=True)