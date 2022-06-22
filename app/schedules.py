from app import app, db, scheduler
from app.controller import PatientController


@scheduler.task('interval', id='do_job_1', days=1, misfire_grace_time=900)
def job1():
    with db.app.app_context():
        PatientController.daily_update()