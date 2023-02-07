import os
import secrets

from flask import url_for, current_app
from flask_mail import Message

from flask_mail import Mail

mail = Mail()


def send_reset_email(user):
    token = user.get_reset_token()
    print(token)
    msg = Message('Password Reset Request',
                  sender='nurbolot664@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('account_api.resettokenresource', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)

