from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_apscheduler import APScheduler

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

jwt = JWTManager(app)

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

from app.model import employee, doctor, patient, appointment
from app import routes, schedules

