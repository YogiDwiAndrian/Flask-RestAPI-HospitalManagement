from app import db
from app.model.enum import Gender
from werkzeug.security import generate_password_hash, check_password_hash

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.Enum(Gender))
    birthdate = db.Column(db.Date)
    work_start_time = db.Column(db.Time, nullable=False)
    work_end_time = db.Column(db.Time, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    doctor_id = db.relationship('Appointment', backref='doctor', lazy='dynamic')

    def __repr__(self):
        return '<Doctor {}>'.format(self.username)

    def setPassword(self, password):
        self.password = generate_password_hash(password)
    
    def checkPassword(self, password):
        return check_password_hash(self.password, password)