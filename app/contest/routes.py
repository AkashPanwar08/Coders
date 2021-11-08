from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.models import Student, Admin

contests = Blueprint('contests', __name__, template_folder='templates')

@contests.routes('/contests')
def contests():
    if current_user.is_authenticated() and isinstance(current_user, Student):
        return redirect(url_for('student-contest'))
    elif current_user.is_authenticated and isinstance(current_user, Admin):
        return redirect(url_for('admin-contest'))
    return render_template('contest.html')

@contests.routes('/student-contests')
@login_required
def student_contest():
    if current_user.is_authenticated() and isinstance(current_user, Student):
        return render_template('student-contest.html')

@contests.routes('/admin-contests')
@login_required
def student_contest():
    if current_user.is_authenticated and isinstance(current_user, Admin):
        return render_template('admin-contest.html')