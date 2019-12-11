from flask import render_template, redirect, request, url_for, flash
from .forms import NewHealthCheckForm
from datetime import datetime, date
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Health_check, User
from .. import db
from . import health_check
from flask_jsonpify import jsonify
from flask import session
import re


@health_check.route('/new_health_check', methods = ['GET','POST'])
@login_required
def new_health_check():
    form = NewHealthCheckForm()
    if form.validate_on_submit():
        pi = session.get("Patient_ID", None)
        print(form.blood_type.data)
        print(form.blood_pressure.data)
        health_check = Health_check(
                    patient_id = pi,
                    physician_id = current_user.user_id,
                    height = form.height.data,
                    weight = form.weight.data,
                    gender = form.gender.data,
                    bmi = ((form.weight.data / form.height.data / form.height.data) * 10000),
                    blood_pressure = form.blood_pressure.data,
                    blood_type = form.blood_type.data,
                    date = datetime.utcnow(),
                    description = form.description.data)
        db.session.add(health_check)
        print(health_check)
        db.session.commit()
        flash('Checkup Sucessful')
        #session.pop("Patient_ID")
        return redirect(url_for('profile.search'))
        #Need to figure out form formatting for where to throw each patient
    return render_template('health_check/new_health_check.html', form = form)
