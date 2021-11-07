from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import bcrypt, login_ip
from app.models import Student, Admin
from flask_login import login_user, logout_user, current_user
from app.login.forms import LoginForm

logins = Blueprint('logins', __name__, template_folder='templates')


@logins.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_anonymous:
        flash('Already logged in', 'success')
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(id=form.username.data).first()
        if student and bcrypt.check_password_hash(student.password, form.password.data):
            login_user(student)
            return redirect(url_for('subjectss.subjects'))
        else:
            flash('Invalid username/password', 'danger') 
    return render_template('login.html', form=form)


@logins.route('/admin-login', methods=['GET', 'POST'])
def adminLogin():
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(id=form.username.data).first()
        if admin and bcrypt.check_password_hash(admin.password, form.password.data):
            login_user(admin)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username/password', 'danger') 
    return render_template('admin-login.html', form=form)


@logins.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
