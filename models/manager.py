from extensions import db

class Manager(db.Model):
    __tablename__ = 'manager_form'
    id = db.Column(db.Integer, primary_key=True)

    emp_table_id = db.Column(db.String(255))


    reply = db.Column(db.String(255))


    IP_addr = db.Column(db.String(255))
    Location = db.Column(db.String(255))
    UserAgent = db.Column(db.String(255))
    OperatingSystem = db.Column(db.String(255))
    Time = db.Column(db.DateTime)