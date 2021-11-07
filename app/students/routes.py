from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import current_user
from app.students.forms import StudentForm, SearchForm, ResetPasswordForm, RequestResetForm
from app import db, bcrypt, login_manager
from app.models import Student,  Solutions, Problems, Subjects, Admin
from app.students.utils import send_reset_email

students = Blueprint('students', __name__, template_folder='templates')


@login_manager.user_loader
def load_student(username):
    if Admin.query.get(username):
        return Admin.query.get(username)
    return Student.query.get((username))


@students.route('/add-students', methods=['GET', 'POST'])
def addstudents():
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        flash('Not valid admin')
        return redirect(url_for('main.index'))
    form = StudentForm()
    if form.validate_on_submit():
        pas = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        student = Student(id=form.id.data, email=form.email.data, password=pas, semester=form.sem.data)
        try:
            db.session.add(student)
            db.session.commit()
            flash('Successfully added', 'success')
            return redirect(url_for('main.homeAdmin'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to add student'+str(e), 'danger')
            return redirect(url_for('students.addstudents'))
    return render_template('add-students.html', form=form)


@students.route('/student-details', methods=['GET', 'POST'])
def studentDetails():
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        flash('Not valid admin')
        return redirect(url_for('main.index'))
    all_student_details = dict()
    students = Student.query.order_by(Student.id)
    for student in students:
        subjects = Subjects.query.filter_by(semester=student.semester).all()
        details = dict()
        status = -1
        for sub in subjects:
            problems = []
            for problem in Problems.query.filter_by(subject_id=sub.id).all():
                try:
                    status = int(Solutions.query.filter_by(user_id=student.id, problem_id=problem.id).first().submitted)
                except:
                    status = -1
                problems.append((problem.title, status))
            details[sub.name] = problems
        all_student_details[student.id] = details
    form = SearchForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(id=form.id.data).first()
        if student == None:
            flash('Student not found', 'danger')
            return redirect(url_for('students.studentDetails', form=form))
        subjects = Subjects.query.filter_by(semester=student.semester).all()
        if subjects == None:
            flash('Subjects not found', 'danger')
            return redirect(url_for('students.studentDetails', form=form))
        details = dict()
        status = -1    # -1 for not attempted 0 for failed attempts and 1 for successfull attempts
        for sub in subjects:
            problems = []
            for problem in Problems.query.filter_by(subject_id=sub.id).all():
                try:
                    status = int(Solutions.query.filter_by(user_id=form.id.data, problem_id=problem.id).first().submitted)
                except:
                    status = -1
                problems.append((problem.title, status))
            details[sub.name] = problems
        return render_template('student-details.html', form=form, details=details, id=form.id.data)
    return render_template('student-details.html', form=form, all_student_details=all_student_details)

@students.route('/reset-request', methods=['GET', 'POST'])
def resetRequest():
    form = RequestResetForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(id=int(form.username.data)).first()
        if student:
            send_reset_email(student)
            flash('An email has been sent with instructions to reset password.', 'info')
            return redirect(url_for('logins.login'))
    return render_template('reset-request.html', form=form)

@students.route('/reset-token-<token>', methods=['GET', 'POST'])
def resetToken(token):
    student = Student.verify_reset_token(token)
    if not student:
        flash('That is an invalid token.', 'warning')
        return redirect(url_for('students.resetRequest'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        student.password = hashed_password
        db.session.commit()
        flash('Your password has been changed! you are now able to login with new password.', 'success')
        return redirect(url_for('logins.login'))
    return render_template('reset_token.html', form=form, token=token)

@students.route('/edit-student-<student_id>', methods=['GET', 'POST'])
def editStudentDetails(student_id):
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        flash('Not valid admin')
        return redirect(url_for('main.index'))
    student = Student.query.filter_by(id=student_id).first()
    form = StudentForm()
    print('validated?')
    if form.validate_on_submit():
        print('validated')
        student.email = form.email.data
        try:
            student.semester = int(form.sem.data)
            flash('Updated successfully.', 'success')
        except Exception as e:
            flash(str(e.message), 'danger')
        try:
            db.session.commit()
        except Exception as e:
            flash(str(e.message), 'danger')
        return redirect(url_for('main.admin'))
    elif request.method == 'GET':
        form.id.data = student_id
        form.email.data = student.email
        form.password.data = student.password
        form.sem.data = student.semester
    return render_template('edit-student.html', form=form, id=student_id)

@students.route('/delete-student-<student_id>', methods=['GET', 'POST'])
def deleteStudent(student_id):
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        flash('Not valid admin')
        return redirect(url_for('main.index'))
    student = Student.query.filter_by(id=student_id).first()
    try:
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('students.studentDetails'))
    except Exception as e:
        flash(str(e))
        db.session.rollback()
    return redirect(url_for('students.deleteStudent', student_id=student_id))
