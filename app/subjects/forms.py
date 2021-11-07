from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length

class SubjectForm(FlaskForm):
    id = StringField('Subject Code', validators=[DataRequired(), Length(min=7, max=8)])
    name = StringField('Name', validators=[DataRequired()])
    discription = StringField('Description', validators=[DataRequired()])
    sem = IntegerField('Semester')
    submit = SubmitField('Submit')