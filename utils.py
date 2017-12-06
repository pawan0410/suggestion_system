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


    msg = Message(subject, sender='info@aigbusiness.in', recipients=[kwargs['escalation']])

    msg.html = """You have one new suggestion from your team member.<br
        Please click on the link below :<br>
        <a href="http://{0}/suggestion/{1}/{2}">Click here</a>
        """.format(request.host,kwargs['id'], kwargs['emp_code'])

    mail.send(msg)

def send_acknowledgement(**kwargs):
    subject = 'Suggestion Form : Acknowledgement'


    msg = Message(subject, sender='info@aigbusiness.in', recipients=[kwargs['emp_email']])

    msg.html = """Your response has been recorded as below : <br>
        Escalation Level - {0} <br>
        Name - {1} <br>
        Employee Code - {2} <br>
        Priority - {3} <br>
        Department - {4} <br>
        Email - {5} <br>
        Type - {6} <br>
        Subject - {7} <br>
        Suggestion - {8} <br>
        """.format(kwargs['escalation'],kwargs['emp_name'],kwargs['emp_code'],kwargs['priority']
                   ,kwargs['department'],kwargs['emp_email'],kwargs['type'],kwargs['issue_subject'],kwargs['suggestion'])

    mail.send(msg)


def send_manager_link_as_mail(**kwargs):
    subject = 'Suggestion form'

    msg = Message(subject, sender='info@aigbusiness.in', recipients=[kwargs['email']])

    msg.html = """Please click on the link below :.<br>
    <a href="http://{0}/final/{1}/{2}">Click here</a>
    """.format(request.host,kwargs['id'], kwargs['emp_code1'])

    mail.send(msg)