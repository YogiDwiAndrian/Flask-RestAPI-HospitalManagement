from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from app.model.employee import Employee
from app import response, app, db
from werkzeug.security import generate_password_hash
import datetime


def login():
    try:
        # accommodate data from POST
        username = request.form.get('username')
        password = request.form.get('password')

        employee = Employee.query.filter_by(username=username).first()

        if not employee:
            return response.badRequestSingle('Username tidak terdaftar')
        
        if not employee.checkPassword(password):
            return response.badRequestSingle('Password tidak sesuai dengan username') 
        

        expires = datetime.timedelta(days=1)
        expires_refresh = datetime.timedelta(days=1)
        
        access_token = create_access_token(identity=username, fresh=True,expires_delta=expires)
        refresh_token = create_refresh_token(identity=username, expires_delta=expires_refresh)

        return response.succes({
            "data" : username,
            "access_token" : access_token,
            "refresh_token" : refresh_token,
        }, 'Login success!')
        
    except Exception as e:
        print(e)

# list of rows object dari employee
def index():
    try:
        # select all data
        employee = Employee.query.all()
        # formating to JSONArray
        data = formatarray(employee)

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
        username = request.form.get('username')
        password = request.form.get('password')

        # create JSONObject
        input = {
            'name' : name,
            'gender' : gender,
            'birthdate' : birthdate,
            'username' : username,
            'password' : generate_password_hash(password)
        }

        # check employee registered
        employee = Employee.query.filter_by(username=username).first()
        if employee:
            return response.badRequestSingle("username has been registered")

        # adding employee to db
        employees = Employee(name=name, gender=gender, birthdate=birthdate, username=username)
        employees.setPassword(password)
        db.session.add(employees)
        db.session.commit()

        return response.succes(input, "succes insert data")
    except Exception as e:
        print(e)

# get detail employee
def detail(id):
    try:
        # query
        employee = Employee.query.filter_by(id=id).first()

        if not employee:
            return response.badRequestSingle('no employee data')
        
        # formating to JSONObject
        data = singleObject(employee)
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
        username = request.form.get('username')
        password = request.form.get('password')

        # create JSONObject
        input = {
            'name' : name,
            'gender' : gender,
            'birthdate' : birthdate,
            'username' : username,
            'password' : generate_password_hash(password)
        }

        employee = Employee.query.filter_by(id=id).first()

        # updating data
        employee.name = name
        employee.gender = gender
        employee.birthdate = birthdate
        employee.username = username
        employee.password = generate_password_hash(password)
        db.session.commit()

        return response.succes(input, "succes update data")

    except Exception as e:
        print(e)

# delete data
def delete(id):
    try:
        # query
        employee = Employee.query.filter_by(id=id).first()
        if not employee:
            return response.badRequestSingle('data not found')
        
        db.session.delete(employee)
        db.session.commit()

        return response.succesSingle('succes delete data!')
    except Exception as e:
        print(e)
