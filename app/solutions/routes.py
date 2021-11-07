from flask import Blueprint, url_for, request, flash, redirect
from flask_login import current_user
from app.models import Solutions
from app import db


solutionss = Blueprint('solutionss', __name__, template_folder='templates')


@solutionss.route('/solution', methods=['GET', 'POST'])
def soltuion():
    if current_user.is_authenticated:
        data = request.get_json()
        try:
            sol = Solutions.query.filter_by(user_id=current_user.id, problem_id=data['problem_id']).first()
            sol.content = data['content']
            sol.monacoLanguageId = data['monaco_language_id']
            sol.judgeLanguageId = data['judge_language_id']
            sol.submitted = data['submitted'] or sol.submitted
            try:
                db.session.commit()
                flash('Solution saved', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Solution failed to be saved', 'danger')
        except:
            sol = Solutions(judgeLanguageId=data['judge_language_id'], monacoLanguageId = data['monaco_language_id'],
                            content = data['content'], submitted = data['submitted'],problem_id = data['problem_id'],
                            user_id = current_user.id)
            try:
                db.session.add(sol)
                db.session.commit()
                flash('Solution saved', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Solution not saved', 'danger')
        return redirect(url_for('main.editor', prblm_id=data['problem_id']))
