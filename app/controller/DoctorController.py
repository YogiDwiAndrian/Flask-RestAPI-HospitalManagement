from app.model.doctor import Doctor
from app import response, db
from flask import request
from werkzeug.security import generate_password_hash

# List of object rows dari doctor
def index():
    try:
        # select all data
        doctor = Doctor.query.all()
        # formating to JSONArray
        data = formatarray(doctor)

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
        'name' : data.name,
        'gender' : data.gender.name,
        'birthdate' : data.birthdate.isoformat(),
        'work_start_time' : data.work_start_time.isoformat(),
        'work_end_time' : data.work_end_time.isoformat(),
        'username' : data.username,
        'password' : data.password
    }
    return data

# insert data
def insert():
    try:
        # accommodate data from POST
        name = request.form.get('name')
        gender = request.form.get('gender')
        birthdate = request.form.get('birthdate')
        work_start_time = request.form.get('work_start_time')
        work_end_time = request.form.get('work_end_time')
        username = request.form.get('username')
        password = request.form.get('password')

        # create JSONObject
        input = {
            'name' : name,
            'gender' : gender,
            'birthdate' : birthdate,
            'work_start_time' : work_start_time,
            'work_end_time' : work_end_time,
            'username' : username,
            'password' : generate_password_hash(password)
        }

        # check doctor registered
        doctor = Doctor.query.filter_by(username=username).first()
        if doctor:
            return response.badRequestSingle("username has been registered")

        # adding doctor to db
        doctors = Doctor(name=name, gender=gender, birthdate=birthdate, work_start_time=work_start_time, work_end_time=work_end_time, username=username)
        doctors.setPassword(password)
        db.session.add(doctors)
        db.session.commit()

        return response.succes(input, "succes insert data")
    except Exception as e:
        print(e)

# get detail doctor
def detail(id):
    try:
        # query
        doctor = Doctor.query.filter_by(id=id).first()

        if not doctor:
            return response.badRequestSingle('no doctor data')
        
        # formating to JSONObject
        data = singleObject(doctor)
        # return JSONObject
        return response.succes(data, "success")
    except Exception as e:
        print(e)


# update data
def update(id):
    try:
        # accommodate data from POST
        name = request.form.get('name')
        gender = request.form.get('gender')
        birthdate = request.form.get('birthdate')
        work_start_time = request.form.get('work_start_time')
        work_end_time = request.form.get('work_end_time')
        username = request.form.get('username')
        password = request.form.get('password')

        # create JSONObject
        input = {
            'name' : name,
            'gender' : gender,
            'birthdate' : birthdate,
            'work_start_time' : work_start_time,
            'work_end_time' : work_end_time,
            'username' : username,
            'password' : generate_password_hash(password)
        }

        doctor = Doctor.query.filter_by(id=id).first()

        # updating data
        doctor.name = name
        doctor.gender = gender
        doctor.birthdate = birthdate
        doctor.work_start_time = work_start_time
        doctor.work_end_time = work_end_time
        doctor.username = username
        doctor.password = generate_password_hash(password)
        db.session.commit()

        return response.succes(input, "succes update data")

    except Exception as e:
        print(e)

# delete data
def delete(id):
    try:
        # query
        doctor = Doctor.query.filter_by(id=id).first()
        if not doctor:
            return response.badRequestSingle('data not found')
        
        db.session.delete(doctor)
        db.session.commit()

        return response.succesSingle('succes delete data!')
    except Exception as e:
        print(e)
