from flask import Flask
from flask import render_template
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/aig_suggestion_system'
app.config['SQLALCHEMY_POOL_SIZE'] = 5
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 120
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280

app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = r'pkaur@aigbusiness.com'
app.config['MAIL_PASSWORD'] = r'#Pawan1#'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db.init_app(app)
mail.init_app(app)

with app.app_context():
    db.create_all()


# def save_signature(base64_str, emp_name, frm_name):
#     path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', emp_name)
#     file_name = '{}_{}.png'.format(path, frm_name)
#     image = base64.b64decode(base64_str.split(',')[1])
#
#     print(image)
#     with open(file_name, 'wb') as f:
#         f.write(image)
#         f.close()
#     return file_name


@app.route("/")
def main():
    return render_template('employee.html')


@app.route("/employee", methods=['POST'])
def save_data():
    emp_name = request.form.get('emp_name')
    emp_code = request.form.get('emp_code')
    emp_email = request.form.get('emp_email')
    priority = request.form.get('priority')
    type = request.form.get('type')
    issue_subject = request.form.get('issue_subject')
    suggestion = request.form.get('suggestion')


    employee_form = Employee(
        emp_code=emp_code,
        emp_name=emp_name,
        emp_email=emp_email,
        priority=priority,
        issue_subject=issue_subject,

        suggestion=suggestion,
        type=type,


        IP_addr=request.remote_addr,
        Location=request.form.get('location'),
        UserAgent=request.user_agent.browser,
        OperatingSystem=request.user_agent.platform,
        Time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

    )

    db.session.add(employee_form)
    db.session.commit()
    utils.send_link_as_mail(
        emp_name=emp_name,


        emp_code=emp_code,

    )
    return redirect('/success')


@app.route("/success")
def success():
    return render_template('thankyou.html')


@app.route("/suggestion/<string:emp_code>")
def suggestion(emp_code):
    the_document = Employee.query.filter(Employee.emp_code == emp_code).order_by("id desc").first()

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # return str(BASE_DIR)

    return render_template('manager.html', the_document=the_document)




@app.route("/manager", methods=['POST'])
def save_managerdata():
    reply = request.form.get('reply')
    emp_code1 = request.form.get('emp_code1')
    email = request.form.get('email')


    manager_form = Manager(

        emp_code1=emp_code1,
        reply=reply,
        email = email,

        IP_addr=request.remote_addr,
        Location=request.form.get('location'),
        UserAgent=request.user_agent.browser,
        OperatingSystem=request.user_agent.platform,
        Time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

    )

    db.session.add(manager_form)
    db.session.commit()
    utils.send_manager_link_as_mail(

        email=email,

        emp_code1=emp_code1,

    )
    return redirect('/success')


@app.route("/final/<string:emp_code1>")
def final_document(emp_code1):
    the_final_document = Manager.query.filter(Manager.emp_code1 == emp_code1
                                              ).order_by("id desc").first()
    the_document = Employee.query.filter(Employee.emp_code == emp_code1
                                         ).order_by("id desc").first()

    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # return str(BASE_DIR)

    return render_template('final.html', the_document=the_document, the_final_document=the_final_document
                           )


# @app.route("/final/<string:emp_code1>/<string:reviewer_code1>",methods=['POST'])
# def save_finaldata(emp_code,reviewer_code):
#    the_document = Employee.query.filter(Employee.emp_code == emp_code,Employee.reviewer_code == reviewer_code).order_by("id desc").first
#    emp_name = the_document.emp_name
#    signature1 = save_signature(request.form.get('signature1'), emp_name, 'signature1')
#
#
#    db.session.execute("""
#                UPDATE Employee SET signaturepath1= signature1 WHERE the_document.emp_code= emp_code
#                """,{'signature1': signature1})
#    db.session.commit()

# @app.route("/final/<string:emp_code1>/<string:reviewer_code1>")
# def final(emp_code1, reviewer_code1):
#     the_final_document = Manager.query.filter(Manager.emp_code1 == emp_code1,
#                                               Manager.reviewer_code1 == reviewer_code1).order_by("id desc").first()
#     the_document = Employee.query.filter(Employee.emp_code == emp_code1,
#                                          Employee.reviewer_code == reviewer_code1).order_by("id desc").first()
#
#     BASE_DIR = os.path.dirname(os.path.abspath(__file__))
#     # return str(BASE_DIR)
#
#     return render_template('finaldocument.html', the_document=the_document, the_final_document=the_final_document,
#                            base_dir=BASE_DIR)
#
#
# @app.route("/save_final", methods=['POST'])
# def save_finaldata(emp_code,reviewer_code):
    # emp_code = request.form['emp_code1']
    # reviewer_code = request.form['reviewer_code1'].strip()
    # the_document = Employee.query.filter(Employee.emp_code==emp_code, Employee.reviewer_code==reviewer_code)
    # emp_code = the_document.emp_code
    # reviewer_code = the_document.reviewer_code
    #
    # the_document = db.session.execute(
    #     """SELECT emp_name from employee_form WHERE reviewer_code='{}' """.format(reviewer_code)).first()
    #
    # emp_name = the_document[0]
    # signature1 = save_signature(request.form.get('signature1'), emp_name, 'signature1')
    #
    # db.session.execute("""
    #                UPDATE employee_form SET signaturepath1='{}' WHERE emp_code='{}'
    #                """.format(signature1, emp_code))
    # db.session.commit()

    # db.session.execute("""
    #             UPDATE employee_form SET signaturepath1= signaturepath1 WHERE emp_code= emp_code
    #             """, {'signaturepath1': signature1, 'emp_code': emp_code})
    # db.session.commit()

    # the_empdocument = Employee.query.filter(Employee.emp_code == emp_code).order_by("id desc").first()
    # the_document = Manager.query.filter(Manager.emp_code1 == emp_code).order_by("id desc").first()
    #
    # file_name = utils.save_document_as_docx(
    #     emp_name=the_empdocument.emp_name,
    #     emp_code=the_empdocument.emp_code,
    #     emp_email=the_empdocument.emp_email,
    #     job_function=the_empdocument.job_function,
    #     date=the_empdocument.date,
    #     reviewer_name=the_empdocument.reviewer_name,
    #     reviewer_code=the_empdocument.reviewer_code,
    #
    #
    #     self_assessment1_comment1=the_empdocument.self_assessment1_comment1,
    #     self_assessment1=the_empdocument.self_assessment1,
    #     manager_assessment1=the_document.manager_assessment1,
    #     manager_assessment1_comment1=the_document.manager_assessment1_comment1,
    #     total_score1=the_document.total_score1,
    #     achieved_score1=the_document.achieved_score1,
    #
    #     self_assessment2_comment2=the_empdocument.self_assessment2_comment2,
    #     self_assessment2=the_empdocument.self_assessment2,
    #     manager_assessment2=the_document.manager_assessment2,
    #     manager_assessment2_comment2=the_document.manager_assessment2_comment2,
    #     total_score2=the_document.total_score2,
    #     achieved_score2=the_document.achieved_score2,
    #
    #     self_assessment3_comment3=the_empdocument.self_assessment3_comment3,
    #     self_assessment3=the_empdocument.self_assessment3,
    #     manager_assessment3=the_document.manager_assessment3,
    #     manager_assessment3_comment3=the_document.manager_assessment3_comment3,
    #     total_score3=the_document.total_score3,
    #     achieved_score3=the_document.achieved_score3,
    #
    #     self_assessment4_comment4=the_empdocument.self_assessment4_comment4,
    #     self_assessment4=the_empdocument.self_assessment4,
    #     manager_assessment4=the_document.manager_assessment4,
    #     manager_assessment4_comment4=the_document.manager_assessment4_comment4,
    #     total_score4=the_document.total_score4,
    #     achieved_score4=the_document.achieved_score4,
    #
    #     self_assessment5_comment5=the_empdocument.self_assessment5_comment5,
    #     self_assessment5=the_empdocument.self_assessment5,
    #     manager_assessment5=the_document.manager_assessment5,
    #     manager_assessment5_comment5=the_document.manager_assessment5_comment5,
    #     total_score5=the_document.total_score5,
    #     achieved_score5=the_document.achieved_score5,
    #
    #     self_assessment6_comment6=the_empdocument.self_assessment6_comment6,
    #     self_assessment6=the_empdocument.self_assessment6,
    #     manager_assessment6=the_document.manager_assessment6,
    #     manager_assessment6_comment6=the_document.manager_assessment6_comment6,
    #     total_score6=the_document.total_score6,
    #     achieved_score6=the_document.achieved_score6,
    #
    #     signature1=the_empdocument.signaturepath1,
    #     signature=the_document.signaturepath,
    #
    # )
    # utils.send_document_as_mail(emp_name=the_empdocument.emp_name, file_name=file_name)

    # return render_template('employee.html', the_empdocument=the_empdocument,the_document= the_document, base_dir=BASE_DIR)
    #return redirect('/success')
