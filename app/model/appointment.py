from app import db
from app.model.patient import Patient
from app.model.doctor import Doctor
from app.model.enum import Status

class Appointment(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey(Patient.id))
    doctor_id = db.Column(db.Integer, db.ForeignKey(Doctor.id))
    datetime = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(Status), nullable=False)
    diagnose = db.Column(db.Text)
    notes = db.Column(db.Text)

    def __repr__(self):
        return '<Appointment {}>'.format(self.id)