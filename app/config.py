import os

class Config:
    SECRET_KEY = '3a1411d68adc82a69aa8634e9f11597b'
    SQLALCHEMY_DATABASE_URI = 'postgresql://87f167d0fc8c:368de994984b@postgres-ae6a01da-bdb1-443b-be0c-9c9eaa8f2018.cqryblsdrbcs.us-east-1.rds.amazonaws.com:2606/PeGBGjnHcUbL'
    #SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/site'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL')
    MAIL_PASSWORD = os.environ.get('PASS')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
