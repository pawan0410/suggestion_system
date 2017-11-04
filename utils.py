import os
import base64
import time



from flask_mail import Message
from flask import render_template
from extensions import mail
from flask import current_app
from flask import request

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')



def send_link_as_mail(**kwargs):
    subject = 'Suggestion Form - {}'.format(kwargs['emp_name'])


    msg = Message(subject, sender='kmt.aigbusiness@gmail.com', recipients=['pkaur@aigbusiness.com'])

    msg.html = """You have one new suggestion from your team member.<br
        Please click on the link below :<br>
        <a href="http://{0}/suggestion/{1}/{2}">Click here</a>
        """.format(request.host,kwargs['id'], kwargs['emp_code'])

    mail.send(msg)



def send_manager_link_as_mail(**kwargs):
    subject = 'Suggestion form'

    msg = Message(subject, sender='pkaur@aigbusiness.com', recipients=[kwargs['email']])

    msg.html = """Please click on the link below :.<br>
    <a href="http://{0}/final/{1}/{2}">Click here</a>
    """.format(request.host,kwargs['id'], kwargs['emp_code1'])

    mail.send(msg)

