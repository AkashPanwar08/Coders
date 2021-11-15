from flask import Blueprint, render_template, url_for, request, flash, redirect
from app.subjects.forms import SubjectForm
from app.models import Subjects, Admin, Semester
from flask_login import current_user, login_required
from app import db

subjectss = Blueprint('subjectss', __name__, template_folder='templates')

@subjectss.route('/subjects')
@login_required
def subjects():
    if isinstance(current_user, Admin):
        return redirect(url_for('subjectss.admin'))
    if not current_user.is_authenticated:
        flash('Please login first', 'danger')
        return redirect(url_for('main.index'))
    return render_template('subjects.html', active3='active', sem=current_user.semester, subjects=Subjects)




@subjectss.route('/admin')
@login_required
def admin():
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        return redirect(url_for('main.index'))
    return render_template('admin.html', subjects=Subjects, semester=Semester, db=db, i=1, active3='active')

@subjectss.route('/admin-new-sub-<int:sem>', methods=['GET', 'POST'])
@login_required
def adminNewSub(sem):
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        flash('Not valid admin')
        return redirect(url_for('main.index'))
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subjects(id=form.id.data,name=form.name.data, discription=form.discription.data, semester=sem)
        try:
            db.session.add(subject)
            db.session.commit()
            flash('Subject added successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Mission Failed' + str(e), 'danger')
            return redirect(url_for('subjectss.adminNewSub', sem=sem))
        return redirect(url_for('subjectss.admin'))
    return render_template('admin-new-sub.html', form=form, sem=sem)



@subjectss.route('/edit-<sub_id>', methods=['Get', 'POST'])
@login_required
def edit(sub_id):
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        flash('Not valid admin')
        return redirect(url_for('main.index'))
    subject = Subjects.query.filter_by(id=sub_id).first()
    form = SubjectForm()
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.discription = form.discription.data
        try:
            subject.semester = int(form.sem.data)
            flash('Updated successfully.', 'success')
        except Exception as e:
            flash(str(e.message), 'danger')
        try:
            db.session.commit()
        except Exception as e:
            flash(str(e.message), 'danger')
        return redirect(url_for('main.admin'))
    elif request.method == 'GET':
        form.id.data = sub_id
        form.name.data = subject.name
        form.discription.data = subject.discription
        form.sem.data = subject.semester
    return render_template('edit.html', form=form, id=sub_id)
    
@subjectss.route('/delete-<sub_id>')
@login_required
def delete(sub_id):
    if not (current_user.is_authenticated and isinstance(current_user, Admin)):
        flash('Not valid admin')
        return redirect(url_for('main.index'))
    sub = Subjects.query.filter_by(id=sub_id).one()
    try:
        db.session.delete(sub)
        db.session.commit()
        flash('Deleted successfully.', 'success')
    except Exception as e:  
        db.session.rollback()
        flash(e)
    return redirect(url_for('subjectss.admin'))
