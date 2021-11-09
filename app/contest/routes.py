from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app.models import Contests, Admin, Student, Questions
from app import db
from app.contest.forms import Contest, Question
from datetime import datetime

contestss = Blueprint('contestss', __name__, template_folder='templates')

@contestss.route('/contests')
def contests():
    if current_user.is_authenticated and isinstance(current_user, Student):
        return redirect(url_for('contestss.student_contest'))
    elif current_user.is_authenticated and isinstance(current_user, Admin):
        return redirect(url_for('contestss.admin_contest'))
    flash('Please login first.', 'danger')
    return redirect(url_for('main.index'))

@contestss.route('/student-contests')
@login_required
def student_contest():
    if current_user.is_authenticated and isinstance(current_user, Student):
        allContests = Contests.query.order_by('startTime')
        return render_template('student-contests.html', active5='active', Contests=allContests, datetime=datetime.now())

@contestss.route('/admin-contests')
@login_required
def admin_contest():
    if current_user.is_authenticated and isinstance(current_user, Admin):
        allContests = Contests.query.order_by('startTime')
        return render_template('admin-contest.html', active5='active', Contests=allContests, datetime=datetime.now())

@contestss.route('/add-contests', methods=['GET', 'POST'])
@login_required
def add_contest():
    if current_user.is_authenticated and isinstance(current_user, Admin):
        form = Contest()
        if form.validate_on_submit():
            if (datetime.now()>form.startTime.data):
                flash('Contest start time is not valid.', 'danger')
            elif (form.startTime.data > form.endTime.data):
                flash('Please check start time and end time.', 'danger')
            else:
                test = Contests(name=form.name.data, startTime=form.startTime.data, endTime=form.endTime.data)
                db.session.add(test)
                try:
                    db.session.commit()
                    flash('Contest created successfully.', 'success')
                    return redirect(url_for('contestss.admin_contest'))
                except Exception as e:
                    flash(str(e), 'danger')
        return render_template('add-contests.html', form=form)

@contestss.route('/add-contest-problems-<id>', methods=['GET', 'POST'])
@login_required
def add_contest_problems(id):
    if current_user.is_authenticated and isinstance(current_user, Admin):
        form = Question()
        if form.validate_on_submit():
            question = Questions(title=form.title.data, body=form.body.data, contest_id=id,testCase=form.testCase.data, testOutput=form.testOutput.data, 
        hiddenCase=form.testCase.data, hiddenOutput=form.hiddenOutput.data)
            db.session.add(question)
            try:
                db.session.commit()
                return redirect(url_for('contestss.admin_contest'))
            except Exception as e:
                flash(str(e), 'danger')
                return redirect(url_for('contestss.add_contest_problems', id=id))
        return render_template('add-contest-problems.html',form=form)