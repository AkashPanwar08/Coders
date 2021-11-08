from app import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask import current_app

class Student(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    semester = db.Column(db.Integer, nullable=False)

    solutions = db.relationship('Solutions', cascade="all,delete", backref='author', lazy=True)

    def get_reset_token(self, expires_sec=180):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Student.query.get(user_id)

    def __repr__(self):
        return f"Student('{self.id}', '{self.semester}')"


class Solutions(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    judgeLanguageId = db.Column(db.Integer, nullable=False)
    monacoLanguageId = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    submitted = db.Column(db.Boolean, default=False)
    
    problem_id = db.Column(db.Integer, db.ForeignKey('problems.id'), nullable=False)
    user_id = db.Column(db.String(20), db.ForeignKey('student.id'), nullable=False)

    def __repr__(self):
        return f"Solution('{self.monacoLanguageId}', '{self.judgeLanguageId}', '{self.content}')"


class Semester(db.Model, UserMixin):
    sem = db.Column(db.Integer, primary_key=True)
    subjects = db.relationship('Subjects', cascade="all,delete", backref='subs', lazy=True)
    

    def __repr__(self):
        return f"Semester('{self.sem}')"

class Subjects(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    discription = db.Column(db.Text, nullable=False)
    
    semester = db.Column(db.Integer, db.ForeignKey('semester.sem'), nullable=False)

    problems = db.relationship('Problems', cascade="all,delete", backref='problems', lazy=True)

    def __repr__(self):
        return f"Subjects('{self.id}', '{self.name}')"


class Problems(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(50), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    testCase = db.Column(db.Text)
    testOutput = db.Column(db.Text, nullable=False)
    hiddenCase = db.Column(db.Text)
    hiddenOutput = db.Column(db.Text, nullable=False)

    subject_id = db.Column(db.String(8), db.ForeignKey('subjects.id'), nullable=False)
    solutions = db.relationship('Solutions', cascade="all,delete", backref='author_', lazy=True)
    
    def __repr__(self):
        return f"Problems('{self.id}', '{self.title}')"

class Admin(db.Model, UserMixin):
    id = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(64), nullable=False)
    
    def __repr__(self):
        return f"Admin('{self.id}', '{self.password}')"

class Contests(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    startTime = db.Column(db.DateTime(), nullable=False)
    endTime = db.Column(db.DateTime(), nullable=False)

    questions = db.relationship('Questions', cascade="all,delete", backref='questions', lazy=True)

class Questions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    body = db.Column(db.Text, nullable=False)

    contest_id = db.Column(db.String(20), db.ForeignKey('contests.id'), nullable=False)

    solutions = db.relationship('ContestSolutions', cascade="all,delete", backref='solutions', lazy=True)

class ContestSolutions(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    judgeLanguageId = db.Column(db.Integer, nullable=False)
    monacoLanguageId = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    student_id = db.Column(db.String(20), db.ForeignKey('register.rollNo'), nullable=False)

class Register(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    contestId = db.Column(db.String(20), nullable=False)
    rollNo = db.Column(db.String(20), nullable=False, unique=True)
    questionId = db.Column(db.Integer())
    submissionTime = db.Column(db.DateTime())
    
    contest_solutions = db.relationship('ContestSolutions', cascade="all,delete", backref='author', lazy=True)

