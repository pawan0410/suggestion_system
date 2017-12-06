from flask import Flask
from flask import render_template
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import send_from_directory
from extensions import db
from extensions import mail
import base64
import os
from flask import request
from flask import redirect
import datetime

from models.employee import Employee
from models.manager import Manager
import utils

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:maria@aig2016@127.0.0.1/aig_suggestion_system'
app.config['SQLALCHEMY_POOL_SIZE'] = 5
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 120
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280

# app.config['MAIL_SERVER'] = 'smtp.office365.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USERNAME'] = r'pkaur@aigbusiness.com'
# app.config['MAIL_PASSWORD'] = r'#Pawan1#'
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = r'info@aigbusiness.in'
app.config['MAIL_PASSWORD'] = r'Qoro1053'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db.init_app(app)
mail.init_app(app)

with app.app_context():
    db.create_all()

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
configure_uploads(app, photos)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

@app.route("/")
def main():
    return render_template('employee.html')

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory(utils.UPLOAD_DIR, filename, as_attachment=True)

@app.route('/view/<path:filename>')
def view_file(filename):
    return send_from_directory(utils.UPLOAD_DIR, filename)

@app.route("/employee", methods=['POST'])
def save_data():

    emp_name = request.form.get('emp_name')
    emp_code = request.form.get('emp_code')
    emp_email = request.form.get('emp_email')
    department = request.form.get('department')
    priority = request.form.get('priority')
    type = request.form.get('type')
    issue_subject = request.form.get('issue_subject')
    suggestion = request.form.get('suggestion')
    escalation = request.form.get('escalation')
    escalation_label = request.form.get('escalation_label')
    final_path = ''

    if 'upload' in request.files:

        filename = photos.save(request.files['upload'])
        final_filename = '{}_{}'.format(emp_code, filename)
        #print(os.path.join(UPLOAD_FOLDER, final_filename))
        final_path = os.path.join(UPLOAD_FOLDER, final_filename)


    employee_form = Employee(

        emp_name=emp_name,
        emp_code=emp_code,
        emp_email=emp_email,
        department=department,
        priority=priority,
        issue_subject=issue_subject,
        suggestion=suggestion,
        type=type,
        escalation=escalation,
        escalation_label=escalation_label,
        image_path=final_path,
        IP_addr=request.remote_addr,
        Location=request.form.get('location'),
        UserAgent=request.user_agent.browser,
        OperatingSystem=request.user_agent.platform,
        Time=datetime.datetime.now() #.strftime("%Y-%m-%d %H:%M:%S"),

    )

    db.session.add(employee_form)
    db.session.commit()

    utils.send_link_as_mail(
        emp_code=emp_code,
        id=employee_form.id,
        emp_name=emp_name,
        escalation=escalation,
        emp_email=emp_email,

    )

    utils.send_acknowledgement(

        emp_email=emp_email,
        emp_name=emp_name,
        emp_code=emp_code,
        department=department,
        priority=priority,
        type=type,
        issue_subject=issue_subject,
        suggestion=suggestion,

        escalation=escalation,

    )

    return redirect('/success')


@app.route("/success")
def success():
    return render_template('thankyou.html')


@app.route("/suggestion/<string:id>/<string:emp_code>")
def suggestion(emp_code,id):
    the_document = Employee.query\
        .filter(Employee.emp_code == emp_code,Employee.id == id).order_by("id desc").first()

    return render_template('manager.html', the_document=the_document, emp_document_id=id, emp_code=emp_code, udir=utils.UPLOAD_DIR)


@app.route("/manager", methods=['POST'])
def save_managerdata():
    emp_document_id = request.form.get('emp_document_id')
    the_document = Employee.query.filter(Employee.id == emp_document_id).order_by("id desc").first()
    reply = request.form.get('reply')

    final_path = ''
    if 'upload1' in request.files:

        filename = photos.save(request.files['upload1'])
        final_filename = '{}_{}'.format(the_document.emp_code, filename)
        #print(os.path.join(UPLOAD_FOLDER, final_filename))
        final_path = os.path.join(UPLOAD_FOLDER, final_filename)

    manager_form = Manager(
        reply=reply,
        emp_table_id=the_document.id,
        image_path=final_path,
        IP_addr=request.remote_addr,
        Location=request.form.get('location'),
        UserAgent=request.user_agent.browser,
        OperatingSystem=request.user_agent.platform,
        Time=datetime.datetime.now()#.strftime("%Y-%m-%d %H:%M:%S"),
    )

    db.session.add(manager_form)
    db.session.commit()
    utils.send_manager_link_as_mail(
        email=the_document.emp_email,
        emp_code1=the_document.emp_code,
        id=the_document.id
    )
    return redirect('/success')


@app.route("/final/<string:id>/<string:emp_code1>")
def final_document(id, emp_code1):
    the_final_document = Manager.query.filter(Manager.emp_table_id == id
                                              ).order_by("id desc").first()
    the_document = Employee.query.filter(Employee.emp_code == emp_code1, Employee.id == id
                                         ).order_by("id desc").first()

    return render_template(
        'final.html', 
        the_document=the_document, 
        the_final_document=the_final_document,
        emp_code=emp_code1,
        udir=utils.UPLOAD_DIR
        )