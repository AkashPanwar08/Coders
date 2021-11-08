from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager
from app.config import Config

login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_ip = dict()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.app_context().push()
    
    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    
    from app.errors.routes import errors
    from app.login.routes import logins
    from app.main.routes import main
    from app.problems.routes import problemss
    from app.solutions.routes import solutionss
    from app.students.routes import students
    from app.subjects.routes import subjectss
    from app.contest.routes import contestss

    app.register_blueprint(errors)
    app.register_blueprint(logins)
    app.register_blueprint(main)
    app.register_blueprint(problemss)
    app.register_blueprint(solutionss)
    app.register_blueprint(students)
    app.register_blueprint(subjectss)
    app.register_blueprint(contestss)

    return app