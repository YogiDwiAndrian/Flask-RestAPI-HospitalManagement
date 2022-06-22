#from folder app import app
from app import app, response
from app.controller import PatientController, EmployeeController, DoctorController, AppoinmentController
from flask import request
from flask_jwt_extended import jwt_required

@app.route('/')
def main():
    return 'Yogi Dwi Andrian'

@app.route('/login', methods=['POST'])
def login():
    return EmployeeController.login()

@app.route('/employees', methods=['GET', 'POST'])
@jwt_required()
def employees():
    if request.method == 'GET':
        return EmployeeController.index()
    elif request.method == 'POST':
        return EmployeeController.insert()

@app.route('/employees/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def employeedetail(id):
    if request.method == 'GET':
        return EmployeeController.detail(id)
    elif request.method == 'PUT':
        return EmployeeController.update(id)
    elif request.method == 'DELETE':
        return EmployeeController.delete(id)

@app.route('/patients', methods=['GET', 'POST'])
@jwt_required()
def patients():
    if request.method == 'GET':
        return PatientController.index()
    elif request.method == 'POST':
        return PatientController.insert()

@app.route('/patients/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def patientdetail(id):
    if request.method == 'GET':
        return PatientController.detail(id)
    elif request.method == 'PUT':
        return PatientController.update(id)
    elif request.method == 'DELETE':
        return PatientController.delete(id)

@app.route('/doctors', methods=['GET', 'POST'])
@jwt_required()
def doctors():
    if request.method == 'GET':
        return DoctorController.index()
    elif request.method == 'POST':
        return DoctorController.insert()

@app.route('/doctors/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def doctordetail(id):
    if request.method == 'GET':
        return DoctorController.detail(id)
    elif request.method == 'PUT':
        return DoctorController.update(id)
    elif request.method == 'DELETE':
        return DoctorController.delete(id)

@app.route('/appointments', methods=['GET', 'POST'])
@jwt_required()
def appointments():
    if request.method == 'GET':
        return AppoinmentController.index()
    if request.method == 'POST':
        return AppoinmentController.insert()

@app.route('/appointments/<id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def appointmentsdetail(id):
    if request.method == 'GET':
        return AppoinmentController.detail(id)
    elif request.method == 'PUT':
        return AppoinmentController.update(id)
    elif request.method == 'DELETE':
        return AppoinmentController.delete(id)

