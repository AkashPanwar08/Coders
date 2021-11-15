from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import current_user, login_required
from app.problems.forms import  ProblemForm
from app.models import Solutions, Problems, Admin
from app import db

problemss = Blueprint('problemss', __name__, template_folder='templates')


@problemss.route('/problems-<sub_id>')
@login_required
def problems(sub_id):
    if not current_user.is_authenticated:
        flash('Please login first', 'danger')
        return redirect(url_for('main.index'))
    if isinstance(current_user, Admin):
        return render_template('admin-problems.html', problems=Problems, sub_id=sub_id)
    else:
        return render_template('problems.html', active3='active', problems=Problems, solution=Solutions, sub_id=sub_id)


@problemss.route('/add-problem-<id>', methods=['GET', 'POST'])
@login_required
def addProblem(id):
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        return redirect(url_for('main.index'))
    form = ProblemForm()
    if form.validate_on_submit():
        problem = Problems(title=form.title.data, content=form.content.data, testCase=form.testCase.data, testOutput=form.testOutput.data, 
        hiddenCase=form.testCase.data, hiddenOutput=form.hiddenOutput.data, subject_id=id)
        try:
            db.session.add(problem)
            db.session.commit()
            flash('Successfully added', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Failed to add', 'danger')
    return render_template('add-problem.html', form=form, id=id)


@problemss.route('/edit-problem-<prblm_id>', methods=['Get', 'POST'])
@login_required
def editProblem(prblm_id):
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        flash('Not valid admin')
        return redirect(url_for('main.index'))
    problem = Problems.query.filter_by(id=prblm_id).first()
    form = ProblemForm()
    if form.validate_on_submit():
        problem.id = prblm_id
        problem.title = form.title.data
        problem.content = form.content.data
        problem.testCase = form.testCase.data
        problem.testOutput = form.testOutput.data
        problem.hiddenCase = form.hiddenCase.data
        problem.hiddenOutput = form.hiddenOutput.data
        try:
            db.session.commit()
            flash('Updated successfull.', 'success')
        except Exception as e:
            flash('Updation failed.', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.title.data = problem.title
        form.content.data = problem.content
        form.testCase.data = problem.testCase
        form.testOutput.data = problem.testOutput
        form.hiddenCase.data = problem.hiddenCase
        form.hiddenOutput.data = problem.hiddenOutput
    return render_template('edit-problems.html', form=form, id=prblm_id)


@problemss.route('/delete-problem-<prblm_id>')
@login_required
def deleteProblem(prblm_id):
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        flash('Not valid admin')
        return redirect(url_for('main.index'))
    sub = Problems.query.filter_by(id=int(prblm_id)).one()
    try:
        db.session.delete(sub)
        db.session.commit()
        flash('Deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()  
        flash(str(e), 'danger')
        flash('Problem ID:'+prblm_id)
    return redirect(url_for('subjectss.admin'))
