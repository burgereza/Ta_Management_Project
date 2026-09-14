from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import db, db_name, db_passWord, db_userName
import models

app = Flask(__name__)
app.secret_key = '1111'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + db_userName + ':' + db_passWord + '@localhost/' + db_name 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
 

@app.route('/')
def index():
    return render_template('index.html')




@app.route('/login_professor', methods=['GET', 'POST'])
def login_professor():
    if request.method == 'POST':
        personnel_code = request.form['personnel_code']
        password = request.form['password']
        
        professor = models.professor.get_professor_by_personnel_code(personnel_code)
        if professor and professor.password == password:
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
        
        student = models.student.get_student_by_student_number(student_number)
        if student and student.password == password:
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




@app.route('/admin1234', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST' and 'add_professor' in request.form:
        personnel_code = request.form['personnel_code']
        name = request.form['professor_name']
        password = request.form['professor_password']
        
        if models.professor.add_professor(personnel_code, name, password):
            flash('استاد با موفقیت اضافه شد')
        else:
            flash('کد پرسنلی تکراری است')
    
    if request.method == 'POST' and 'add_student' in request.form:
        student_number = request.form['student_number']
        name = request.form['student_name']
        password = request.form['student_password']
        
        if models.student.add_student(student_number, name, password):
            flash('دانشجو با موفقیت اضافه شد')
        else:
            flash('شماره دانشجویی تکراری است')
    
    if request.method == 'POST' and 'add_course_name' in request.form:
        code = request.form['course_code']
        name = request.form['course_name']
        
        if models.course_name.add_course_name(code, name):
            flash('درس پایه با موفقیت اضافه شد')
        else:
            flash('کد درس تکراری است')
    
    return render_template('admin_panel.html')




@app.route('/professor_dashboard')
def professor_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    professor_id = session['user_id']

    section = request.args.get('section')

    if section == 'profile':
        return render_template('professor_dashboard.html', section='profile')

    if section == 'add_course':
        course_names = models.course_name.get_all_course_names()
        return render_template('professor_dashboard.html' ,section='add_course' ,course_names=course_names)

    courses = models.course.get_courses_by_professor(professor_id)
    return render_template('professor_dashboard.html', section='courses', courses=courses)




@app.route('/add_course', methods=['POST'])
def add_course():
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    professor_id = session['user_id']
    course_code = request.form['course_code']
    term = request.form['term']

    course_name = models.course_name.get_course_name_by_code(course_code)

    if models.course.get_course_by_code_professor_term(course_code, professor_id, term):
        flash('این درس قبلاً در این ترم اضافه شده است')
        return redirect(url_for('professor_dashboard'))
    
    models.course.add_course_for_professor(course_code, course_name, professor_id, term)
    flash('درس با موفقیت اضافه شد')
    
    return redirect(url_for('professor_dashboard'))




@app.route('/professor_course')
def professor_course():
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    professor_id = session['user_id']
    course_code = request.args.get('course_code')
    term = request.args.get('term')
    
    course = models.course.get_course_by_code_professor_term(course_code, professor_id, term)

    pending = models.request.get_requests_students_by_course(course_code, professor_id, term, 'pending')
    accepted = models.request.get_requests_students_by_course(course_code, professor_id, term, 'accepted')
    
    return render_template('professor_course.html', course=course, pending=pending, accepted=accepted)




@app.route('/accept_request/<int:request_id>')
def accept_request(request_id):
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    request = models.request.get_request_by_id(request_id)
    models.request.update_request_status(request_id, 'accepted')
    flash('درخواست با موفقیت پذیرفته شد')
    
    return redirect(url_for('professor_course', course_code=request.course_code, term=request.term))  




@app.route('/student_ta_history/<student_id>')
def student_ta_history(student_id):
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    student = models.student.get_student_by_student_number(student_id)

    reviews_with_details = models.review.get_reviews_with_details_by_student_number(student_id)

    requests_with_details = models.request.get_student_requests_with_details_by_student_number(student_id)
    
    return render_template('student_ta_history.html', student=student, reviews=reviews_with_details, requests=requests_with_details)




@app.route('/change_professor_password', methods=['POST'])
def change_professor_password_route():
    if 'user_id' not in session:
        return redirect(url_for('login_professor'))

    professor_id = session['user_id']

    old_password = request.form['old_password']
    new_password = request.form['new_password']
    
    if models.professor.update_professor_password(professor_id, old_password, new_password):
        flash('رمز عبور با موفقیت تغییر کرد')
    else:
        flash('رمز عبور قبلی نادرست است')
    
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
        courses_for_review = models.request.get_courses_for_review(student_id)
        return render_template('student_dashboard.html', section='review', courses=courses_for_review)

    courses_with_status = models.request.get_courses_with_status_for_student(student_id)
    
    return render_template('student_dashboard.html', section='courses', courses=courses_with_status)




@app.route('/request_ta')
def request_ta():
    if 'user_id' not in session:
        return redirect(url_for('login_student'))

    student_id = session['user_id']

    course_code = request.args.get('course_code')
    professor_id = request.args.get('professor_id')
    term = request.args.get('term')

    if models.request.get_request_by_student_and_course(student_id, course_code, professor_id, term):
        flash('شما قبلاً برای این درس درخواست داده‌اید')
        return redirect(url_for('student_dashboard'))
    
    models.request.add_new_request(student_id, course_code, professor_id, term, 'pending')
    flash('درخواست شما با موفقیت ثبت شد')
    
    return redirect(url_for('student_dashboard'))




@app.route('/review_course')
def review_course():
    if 'user_id' not in session:
        return redirect(url_for('login_student'))

    course_code = request.args.get('course_code')
    professor_id = request.args.get('professor_id')
    term = request.args.get('term')
    
    course = models.course.get_course_by_code_professor_term(course_code, professor_id, term)
    professor_name = models.professor.get_professor_by_personnel_code(professor_id).name

    accepted_requests = models.request.get_accepted_requests_for_course(course_code, professor_id, term)
    tas = []
    for req in accepted_requests:
        student_obj = models.student.get_student_by_student_number(req.student_id)
        if student_obj:
            tas.append(student_obj)
    
    return render_template('review.html', course=course, tas=tas, professor_name=professor_name)




@app.route('/add_review', methods=['POST'])
def add_review():
    if 'user_id' not in session:
        return redirect(url_for('login_student'))

    reviewer_id = session['user_id']

    ta_id = request.form['ta_id']
    course_code = request.form['course_code']
    professor_id = request.form['professor_id']
    term = request.form['term']
    rating = int(request.form['rating'])
    comment = request.form['comment']

    if models.review.check_student_review_for_course(ta_id, course_code, professor_id, term, reviewer_id):
        flash('شما قبلاً برای این دستیار در این درس نظر ثبت کرده‌اید')
        return redirect(url_for('review_course', course_code=course_code, professor_id=professor_id, term=term))

    models.review.add_new_review(ta_id, course_code, professor_id, term, reviewer_id, rating, comment)
    flash('نظر شما با موفقیت ثبت شد')
    
    return redirect(url_for('student_dashboard', section='review'))




@app.route('/change_student_password', methods=['POST'])
def change_student_password_route():
    if 'user_id' not in session:
        return redirect(url_for('login_student'))

    student_id = session['user_id']

    old_password = request.form['old_password']
    new_password = request.form['new_password']
    
    if models.student.update_student_password(student_id, old_password, new_password):
        flash('رمز عبور با موفقیت تغییر کرد')
    else:
        flash('رمز عبور قبلی نادرست است')
    
    return redirect(url_for('student_dashboard', section='profile'))


if __name__ == '__main__':
    app.run(debug=True)