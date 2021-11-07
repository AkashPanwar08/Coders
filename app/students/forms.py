from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from app.models import Student

class StudentForm(FlaskForm):
    id = StringField('Student ID', validators=[DataRequired(), Length(min=10, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired(), Length(min=4, max=20)])
    sem = IntegerField('Semester', validators=[DataRequired()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    id = StringField('Student ID', validators=[DataRequired(), Length(min=10, max=20)])
    submit = SubmitField('Search')

class RequestResetForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20, min=10)])
    submit = SubmitField('Request Password Reset')

    def validate_username(self, username):
        student = Student.query.filter_by(id=username.data).first()
        if student is None:
            raise ValidationError('This username does not exist')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirmPassword', message='Passwords must match')])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reset Password')