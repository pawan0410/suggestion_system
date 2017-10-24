from extensions import db

class Employee(db.Model):
    __tablename__ = 'employee_form'
    id = db.Column(db.Integer, primary_key=True)
    emp_name = db.Column(db.String(255))

    emp_code = db.Column(db.String(255))

    priority = db.Column(db.String(255))

    # date = db.Column(db.Date)

    type = db.Column(db.String(255))

    issue_subject = db.Column(db.String(255))
    suggestion = db.Column(db.String(255))





    IP_addr = db.Column(db.String(255))
    Location = db.Column(db.String(255))
    UserAgent = db.Column(db.String(255))
    OperatingSystem = db.Column(db.String(255))
    Time = db.Column(db.DateTime)