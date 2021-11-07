from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ProblemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    testCase = TextAreaField('Sample Test Case Input')
    testOutput = TextAreaField('Sample Test Case Output', validators=[DataRequired()])
    hiddenCase = TextAreaField('Hidden Test Case Input')
    hiddenOutput = TextAreaField('Hidden Test Case Output')
    submit = SubmitField('Submit')
