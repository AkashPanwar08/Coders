from flask_mail import Message
from app import mail
from flask import url_for


def send_reset_email(student):
    token = student.get_reset_token()
    msg = Message('Password Reset Request', 
                    sender='noreply@demo.com', 
                    recipients=[student.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('students.resetToken', token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
'''
    mail.send(msg)
