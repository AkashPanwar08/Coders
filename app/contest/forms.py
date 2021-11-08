from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, SubmitField, IntegerField
from wtforms.fields.html5 import DateTimeLocalField


class Contests(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=20)])
    startTime = DateTimeLocalField('Start Time', validators=[DataRequired()])
    endTime = DateTimeLocalField('Finish Time', validators=[DataRequired()])
    submit = SubmitField('Submit')

class Question(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = StringField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')