import imp
from app.model.patient import Patient
from app.model.appointment import Appointment
from app import response, db
from flask import request

from google.cloud import bigquery
from google.oauth2 import service_account
import json

# List of object rows dari patient
def index():
    try:
        # select all data
        patient = Patient.query.all()
        # formating to JSONArray
        data = formatarray(patient)

        # return JSONObject 
        return response.succes(data, "succes")
    except Exception as e:
        print(e)

def formatarray(datas):
    # create JSONArray
    array = []
    for i in datas:
        array.append(singleObject(i))

    return array


def singleObject(data):
    # create JSONOBject
    data = {
        'id' : data.id,
        'no_ktp' : data.no_ktp,
        'name' : data.name,
        'gender' : data.gender.name,
        'birthdate' : data.birthdate.isoformat(),
        'address' : data.address,
        'vaccine_type' : data.vaccine_type,
        'vaccine_count' : data.vaccine_count,
    }
    return data

# insert data
def insert():
    try:
        # accommodate data from POST
        no_ktp = request.form.get('no_ktp')
        name = request.form.get('name')
        gender = request.form.get('gender')
        birthdate = request.form.get('birthdate')
        address = request.form.get('address')
        vaccine_type = request.form.get('vaccine_type')
        vaccine_count = request.form.get('vaccine_count')

        # create JSONObject
        input = {
            'no_ktp' : no_ktp,
            'name' : name,
            'gender' : gender,
            'birthdate' : birthdate,
            'address' : address,
            'vaccine_type' : vaccine_type,
            'vaccine_count' : vaccine_count,
        }

        # check no ktp registered
        patient = Patient.query.filter_by(no_ktp=no_ktp).first()
        if patient:
            return response.badRequestSingle("KTP has been registered")

        # adding patient to db
        patients = Patient(no_ktp=no_ktp, name=name, gender=gender, birthdate=birthdate, address=address, vaccine_type=vaccine_type, vaccine_count=vaccine_count)
        db.session.add(patients)
        db.session.commit()

        return response.succes(input, "succes insert data")
    except Exception as e:
        print(e)

# get detail patient
def detail(id):
    try:
        # query
        patient = Patient.query.filter_by(id=id).first()
        appointment = Appointment.query.filter(Appointment.patient_id==id)

        if not patient:
            return response.badRequestSingle('no employee data')
        
        # formating appoinment to JSONArray
        med_hist = formatAppoinment(appointment)
        
        # formating JSONObject and adding JSONArray inside it
        data = singleDetailPatient(patient, med_hist)

        # return JSONObject
        return response.succes(data, "success")
    except Exception as e:
        print(e)

def singleDetailPatient(patient, med_hist):
    # create JSONOBject
    data = {
        'no_ktp' : patient.no_ktp,
        'name' : patient.name,
        'gender' : patient.gender.name,
        'birthdate' : patient.birthdate.isoformat(),
        'address' : patient.address,
        'vaccine_type' : patient.vaccine_type,
        'vaccine_count' : patient.vaccine_count,
        'medical_history' : med_hist
    }

    return data

def singleAppoinment(appointment):
    # create JSONOBject
    data = {
        'doctor_id': appointment.doctor_id,
        'datetime': appointment.datetime,
        'status': appointment.status.name,
        'diagnose': appointment.diagnose,
        'notes': appointment.notes
    }

    return data

def formatAppoinment(data):
    # create JSONArray
    array = []
    for i in data:
        array.append(singleAppoinment(i))
    return array

# update data
def update(id):
    try:
        # accommodate data from POST
        no_ktp = request.form.get('no_ktp')
        name = request.form.get('name')
        gender = request.form.get('gender')
        birthdate = request.form.get('birthdate')
        address = request.form.get('address')
        vaccine_type = request.form.get('vaccine_type')
        vaccine_count = request.form.get('vaccine_count')

        # create JSONObject
        input = {
            'no_ktp' : no_ktp,
            'name' : name,
            'gender' : gender,
            'birthdate' : birthdate,
            'address' : address,
            'vaccine_type' : vaccine_type,
            'vaccine_count' : vaccine_count
        }

        patient = Patient.query.filter_by(id=id).first()

        # updating data
        patient.no_ktp = no_ktp
        patient.name = name
        patient.gender = gender
        patient.birthdate = birthdate
        patient.address = address
        patient.vaccine_type = vaccine_type
        patient.vaccine_count = vaccine_count
        db.session.commit()

        return response.succes(input, "succes update data")

    except Exception as e:
        print(e)

# delete data
def delete(id):
    try:
        # query
        patient = Patient.query.filter_by(id=id).first()
        if not patient:
            return response.badRequestSingle('data not found')
        
        db.session.delete(patient)
        db.session.commit()

        return response.succesSingle('succes delete data!')
    except Exception as e:
        print(e)
        
def daily_update():
    try:
        # select all data
        patient = Patient.query.all()
        # formating to JSONArray
        job_update(patient, bigQuery())
    except Exception as e:
        print(e)

def job_update(datasql, databq):
    # iterate result data from local db
    for i in datasql:
        # iterate result data from bigquery
        for j in databq:
            if i.no_ktp == dict(j)['no_ktp']:
                patient = Patient.query.filter_by(no_ktp=i.no_ktp).first()
                # updating data
                patient.vaccine_type = dict(j)['vaccine_type']
                patient.vaccine_count = dict(j)['vaccine_count']
                db.session.commit()
                print('success updated')

def bigQuery():
    # google api credentials to acces bigquery
    credentials = service_account.Credentials.from_service_account_file('delman.json')

    client = bigquery.Client(location="US")

    project_id = 'delman-interview'
    client = bigquery.Client(credentials= credentials,project=project_id)

    query = """
        SELECT *
        FROM `delman-interview.interview_mock_data.vaccine-data`
    """
    
    query_job = client.query(
        query
    )  # API request - starts the query

    return query_job
