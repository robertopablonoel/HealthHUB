from flask import render_template, redirect, request, url_for, flash
from . import sched
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Patient, User, Physician_schedule, Physician, Permission
from .. import db
from .forms import PatientAppointmentForm
from datetime import date
from dateutil.relativedelta import relativedelta
import re

@sched.route('/schedule', methods = ['GET','POST'])
@login_required
def schedule():
    form = PatientAppointmentForm()
    physicians = Physician.query.join(User).filter_by(hospital_id = current_user.hospital_id).all()
    physician_users = User.query.filter(User.user_id.in_([ret.user_id for ret in physicians])).all()
    form.physician.choices = [(ret.user_id, "Dr. {} {}".format(ret.first_name,ret.last_name) ) for ret in physician_users]
    physician_schedule = Physician_schedule.query.filter(Physician_schedule.physician_id.in_([ret.user_id for ret in physicians])).filter(Physician_schedule.start_time >= date.today()).filter(Physician_schedule.end_time <= (date.today() + relativedelta(months=1))).order_by(Physician_schedule.start_time.asc()).all()
    form.purpose.choices = [(0,'Check-up'), (1, 'Sickness'), (2, 'Other')]
    form.time_slot.choices = [(ret.physician_id, "{} to {}".format(ret.start_time,ret.end_time)) for ret in physician_schedule]
    if form.validate_on_submit():
        time_slot = dict(form.time_slot.choices).get(form.time_slot.data).split(" to ")
        event_type = dict(form.purpose.choices).get(form.purpose.data)
        event = Physician_schedule(physician_id = form.physician.data,
                                    start_time = time_slot[0],
                                    end_time = time_slot[1],
                                    event_type = event_type)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for("main.index"))
    print("Form >>> ", form, '\n')
    print("Phyician schedule >>> ", physician_schedule, '\n')
    print("Permissions >>> ", Permission, '\n')
    return render_template('sched/schedule.html', form = form, physician_schedule = physician_schedule, permissions = Permission)

#Here comes the scheduling code...
