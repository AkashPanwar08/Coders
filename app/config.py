import os

class Config:
    SECRET_KEY = os.environ.get('SEC_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/site'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('PASS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
