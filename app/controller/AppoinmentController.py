from app.model.appointment import Appointment
from app.model.doctor import Doctor
from app.model.patient import Patient
from app import response, db
from flask import request
from datetime import datetime

def index():
    try:
        appoinment = Appointment.query.all()
        data = formatarray(appoinment)
        return response.succes(data, "succes")
    except Exception as e:
        print(e)

def formatarray(datas):
    array = []

    for i in datas:
        array.append(singleObject(i))

    return array


def singleObject(data):
    data = {
        'id' : data.id,
        'patient_id' : data.patient_id,
        'doctor_id' : data.doctor_id,
        'datetime' : data.datetime.isoformat(),
        'status' : data.status.name,
        'diagnose' : data.diagnose,
        'notes' : data.notes
    }
    return data

# insert data
def insert():
    try:
        # accommodate data from POST
        patient_id = request.form.get('patient_id')
        doctor_id = request.form.get('doctor_id')
        dt = request.form.get('datetime')
        status = request.form.get('status')
        diagnose = request.form.get('diagnose')
        notes = request.form.get('notes')

        # create JSONObject
        input = {
            'patient_id' : patient_id,
            'doctor_id' : doctor_id,
            'datetime' : dt,
            'status' : status,
            'diagnose' : diagnose,
            'notes' : notes,
        }
        
        patient = Patient.query.filter_by(id=patient_id).first()
        doctor = Doctor.query.filter_by(id=doctor_id).first()

        if not patient:
            return response.succesSingle('patient ID unkown')

        if not doctor:
            return response.succesSingle('doctor ID unkown')
        
        # doctor working hours
        start_working = doctor.work_start_time
        end_working = doctor.work_end_time
        
        # plan appoinment
        time_plan = datetime.fromisoformat(dt).time()

        # validate working hours doctor
        if time_plan < start_working or time_plan > end_working:
            return response.succesSingle("There are no doctor's working hours")

        # validate bboking status       
        booked = Appointment.query.filter_by(doctor_id=doctor_id, datetime=dt).first()
        if booked:
            return response.succesSingle("the appointment has already been booked")
        
        # adding appoinment to db
        appoinment = Appointment(patient_id=patient_id, doctor_id=doctor_id, status=status, datetime=dt, diagnose=diagnose, notes=notes)
        db.session.add(appoinment)
        db.session.commit()

        return response.succes(input, "succes insert data") 
    except Exception as e:
        print(e)

# get detail doctor
def detail(id):
    try:
        # query
        appointment = Appointment.query.filter_by(id=id).first()

        if not appointment:
            return response.badRequestSingle('no appointment record')
        
        # formating to JSONObject
        data = singleObject(appointment)
        # return JSONObject
        return response.succes(data, "success")
    except Exception as e:
        print(e)

# update data
def update(id):
    try:
        # accommodate data from POST
        patient_id = request.form.get('patient_id')
        doctor_id = request.form.get('doctor_id')
        dt = request.form.get('datetime')
        status = request.form.get('status')
        diagnose = request.form.get('diagnose')
        notes = request.form.get('notes')

        # create JSONObject
        input = {
            'patient_id' : patient_id,
            'doctor_id' : doctor_id,
            'datetime' : dt,
            'status' : status,
            'diagnose' : diagnose,
            'notes' : notes
        }

        appointment = Appointment.query.filter_by(id=id).first()

        # updating data
        appointment.patient_id = patient_id
        appointment.doctor_id = doctor_id
        appointment.datetime = dt
        appointment.status = status
        appointment.diagnose = diagnose
        appointment.notes = notes
        db.session.commit()

        return response.succes(input, "succes update data")

    except Exception as e:
        print(e)

# delete data
def delete(id):
    try:
        # query
        appointment = Appointment.query.filter_by(id=id).first()
        if not appointment:
            return response.badRequestSingle('data not found')
        
        db.session.delete(appointment)
        db.session.commit()

        return response.succesSingle('succes delete data!')
    except Exception as e:
        print(e)

