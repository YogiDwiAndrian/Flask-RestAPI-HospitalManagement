from app import db
from app.model.enum import Gender

class Patient(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    no_ktp = db.Column(db.BigInteger, unique=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.Enum(Gender))
    birthdate = db.Column(db.Date, nullable=False)
    address = db.Column(db.Text, nullable=False)
    vaccine_type  = db.Column(db.String(32))
    vaccine_count  = db.Column(db.SmallInteger)

    patient_id = db.relationship('Appointment', backref='patient', lazy='dynamic')

    def __repr__(self):
        return '<Patient {}>'.format(self.no_ktp)
    