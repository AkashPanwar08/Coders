from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateTimeLocalField


class Contest(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    startTime = DateTimeLocalField('Start Time', validators=[DataRequired()], format=f'%Y-%m-%dT%H:%M')
    endTime = DateTimeLocalField('Finish Time', validators=[DataRequired()], format=f'%Y-%m-%dT%H:%M')
    submit = SubmitField('Submit')

class Question(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    testCase = TextAreaField('Sample Test Case Input')
    testOutput = TextAreaField('Sample Test Case Output', validators=[DataRequired()])
    hiddenCase = TextAreaField('Hidden Test Case Input')
    hiddenOutput = TextAreaField('Hidden Test Case Output')
    submit = SubmitField('Submit')