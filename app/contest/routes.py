from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user, login_required
from app.models import Contests, Admin, Student, Questions, Register, ContestSolutions
from app import db, login_manager
from app.contest.forms import Contest, Question
from datetime import datetime
from app.codes import languages
from flask_paginate import Pagination, get_page_parameter

contestss = Blueprint('contestss', __name__, template_folder='templates')

@contestss.route('/contests')
@login_required
def contests():
    if current_user.is_authenticated and isinstance(current_user, Student):
        return redirect(url_for('contestss.studentContest'))
    elif current_user.is_authenticated and isinstance(current_user, Admin):
        return redirect(url_for('contestss.adminContest'))
    flash('Please login first.', 'danger')
    return redirect(url_for('main.index'))

@contestss.route('/student-contests')
@login_required
def studentContest():
    if current_user.is_authenticated and isinstance(current_user, Student):
        allContests = Contests.query.order_by('startTime')
        return render_template('student-contests.html', active5='active', Contests=allContests, register=Register(), id=current_user.id, datetime=datetime.now())

@contestss.route('/admin-contests')
@login_required
def adminContest():
    if current_user.is_authenticated and isinstance(current_user, Admin):
        allContests = Contests.query.order_by('startTime')
        return render_template('admin-contest.html', active5='active', Contests=allContests, datetime=datetime.now())

@contestss.route('/add-contests', methods=['GET', 'POST'])
@login_required
def addContest():
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
                    return redirect(url_for('contestss.adminContest'))
                except Exception as e:
                    flash(str(e), 'danger')
        return render_template('add-contests.html', form=form)

@contestss.route('/add-contest-problems-<id>', methods=['GET', 'POST'])
@login_required
def addContestProblems(id):
    if current_user.is_authenticated and isinstance(current_user, Admin):
        form = Question()
        if form.validate_on_submit():
            question = Questions(title=form.title.data, body=form.body.data, contest_id=id,testCase=form.testCase.data, testOutput=form.testOutput.data, 
        hiddenCase=form.hiddenCase.data, hiddenOutput=form.hiddenOutput.data)
            db.session.add(question)
            try:
                db.session.commit()
                return redirect(url_for('contestss.adminContest'))
            except Exception as e:
                flash(str(e), 'danger')
                return redirect(url_for('contestss.addContestProblems', id=id))
        return render_template('add-contest-problems.html',form=form)

@contestss.route('/edit-contest-<id>', methods=['GET', 'POST'])
@login_required
def editContest(id):
    if current_user.is_authenticated and isinstance(current_user, Admin):
        form = Contest()
        contest = Contests.query.filter_by(id=id).first()
        if form.validate_on_submit():
            contest.id = id
            contest.name = form.name.data
            contest.startTime = form.startTime.data
            contest.endTime = form.endTime.data
            db.session.commit()
            return redirect(url_for('contestss.contests'))
        elif request.method == 'GET':
            form.name.data = contest.name
            form.startTime.data = contest.startTime
            form.endTime.data = contest.endTime
        return render_template('edit-contest.html', form=form)

@contestss.route('/contest-problems-<id>', methods=['GET', 'POST'])
@login_required
def contestProblems(id):
    if current_user.is_authenticated and isinstance(current_user, Admin):
        questions = Questions.query.filter_by(contest_id=id).all()
        return render_template('contest-problems.html', questions=questions, contest_id=id)

@contestss.route('/edit-contest-problems-<id>', methods=['GET', 'POST'])
@login_required
def editContestQuestion(id):
    if current_user.is_authenticated and isinstance(current_user, Admin):
        form = Question()
        question = Questions.query.filter_by(id=id).first()
        if form.validate_on_submit():
            question.id = id
            question.title = form.title.data
            question.body = form.body.data
            question.testCase = form.testCase.data
            question.testOutput = form.testOutput.data
            question.hiddenCase = form.hiddenCase.data
            question.hiddenOutput = form.hiddenOutput.data
            try:
                db.session.commit()
                flash('Updated successfull.', 'success')
            except Exception as e:
                flash('Updation failed.', 'success')
            return redirect(url_for('contestss.contests'))
        elif request.method == 'GET':
            form.title.data = question.title
            form.body.data = question.body
            form.testCase.data = question.testCase
            form.testOutput.data = question.testOutput
            form.hiddenCase.data = question.hiddenCase
            form.hiddenOutput.data = question.hiddenOutput
        return render_template('edit-contest-problem.html', form=form,id=id)


@contestss.route('/delete-contest-problem-<prblm_id>')
@login_required
def deleteContestProblem(prblm_id):
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        flash('Not valid admin')
        return redirect(url_for('main.index'))
    que = Questions.query.filter_by(id=int(prblm_id)).one()
    try:
        db.session.delete(que)
        db.session.commit()
        flash('Deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()  
        flash(str(e), 'danger')
        flash('Problem ID:'+prblm_id)
    return redirect(url_for('contestss.contests'))

@contestss.route('/delete-contest-<contest_id>', methods=['GET', 'POST'])
@login_required
def deleteContest(contest_id):
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        flash('Not valid admin')
        return redirect(url_for('main.index'))
    contest = Contests.query.filter_by(id=contest_id).first()
    try:
        db.session.delete(contest)
        db.session.commit()
        return redirect(url_for('contestss.contests'))
    except Exception as e:
        flash(str(e))
        db.session.rollback()
    return redirect(url_for('students.deleteContest', contest_id=contest_id))

@contestss.route('/register-<contest_id>', methods=['GET', 'POST'])
@login_required
def register(contest_id):
    if not (current_user.is_authenticated and isinstance(current_user, Student)):
        flash('Please login with student ID')
        return redirect(url_for('main.login'))
    regi = Register(contestId=contest_id, rollNo=current_user.id)
    db.session.add(regi)
    db.session.commit()
    return redirect(url_for('contestss.contests'))

@contestss.route('/start-contest-<contest_id>', methods=['GET', 'POST'])
@login_required
def startContest(contest_id):
    if not (current_user.is_authenticated and isinstance(current_user, Student)):
        flash('Please login with student ID')
        return redirect(url_for('main.login'))
    con = Contests.query.filter_by(id=contest_id).first()
    if con.startTime < datetime.now() and con.endTime > datetime.now():
        questions = Questions.query.filter_by(contest_id=contest_id).all()
        return render_template('start-contest.html', questions=questions, solution=ContestSolutions, contest_id=contest_id)
    else:
        flash('This contest can not be started right now.', 'danger')
        return redirect(url_for('contestss.contests'))

@contestss.route('/contest-editor-<question_id>-<contest_id>', methods=['GET', 'POST'])
@login_required
def contestEditor(question_id, contest_id):
    if not (current_user.is_authenticated and isinstance(current_user, Student)):
        flash('Please login with student ID')
        return redirect(url_for('main.login'))
    problem=Questions.query.filter_by(id=question_id).first()
    return render_template('contest-editor.html', languages=languages, problem=problem, id=current_user.id,contest_id=contest_id)

@contestss.route('/contest-solution', methods=['GET', 'POST'])
@login_required
def contestSoltuion():
    if current_user.is_authenticated:
        data = request.get_json()
        try:
            sol = ContestSolutions.query.filter_by(student_id=current_user.id, question_id=data['problem_id']).first()
            sol.content = data['content']
            sol.monacoLanguageId = data['monaco_language_id']
            sol.judgeLanguageId = data['judge_language_id']
            sol.submitted = data['submitted'] or sol.submitted
            sol.submitTime = sol.submitTime
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
        except:
            sol = ContestSolutions(judgeLanguageId=data['judge_language_id'], monacoLanguageId = data['monaco_language_id'],
                            content = data['content'], submitted = data['submitted'],question_id = data['problem_id'],
                            student_id = current_user.id, submitTime=datetime.now())
            regis = Register.query.filter_by(rollNo=current_user.id, contestId=data['contest_id']).first()
            regis.submitTime = datetime.now()
            regis.count+=1
            try:
                db.session.add(sol)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
        return redirect(url_for('contestss.contestEditor', question_id=data['problem_id'], contest_id=data['contest_id']))

@contestss.route('/contest-ranks-<contest_id>', methods=['GET', 'POST'])
@login_required
def contestRanks(contest_id):
    if not (current_user.is_authenticated and isinstance(current_user, Student)):
        flash('Please login with student ID')
        return redirect(url_for('main.login'))

    search = False
    q = request.args.get('q')
    if q:
        search = True
    PAGE_SIZE = 10
    page = request.args.get(get_page_parameter(), type=int, default=1)

    ranks = Register.query.filter_by(contestId=contest_id).order_by(Register.count.desc(), Register.submitTime)

    pagination = Pagination(page=page, total=ranks.count(), search=search, inner_window=1, outer_window=0, record_name='ranks', per_page=PAGE_SIZE)

    ranks = ranks.paginate(page=page, per_page=PAGE_SIZE)

    return render_template('contest-ranks.html', ranks=ranks, pagination=pagination)

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Please login first.', 'danger')
    return redirect('/login')