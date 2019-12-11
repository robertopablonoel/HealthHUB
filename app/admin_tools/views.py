from flask import render_template, redirect, request, url_for, flash
from .forms import
from datetime import datetime, date
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Physician, Nurse, User
from .. import db
from . import profile
from flask_jsonpify import jsonify
from flask import session
import re

@profile.route('/set_search')
@login_required
def set_search():
    if session.get("Patient_ID") != None:
        session.pop("Patient_ID")
    return redirect(url_for('profile.search'))

@profile.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
    print(session.get("Patient_ID"))
    if session.get("Patient_ID") == None:
        return render_template('profile/search_patient.html')
    user_id = session.get("Patient_ID")
    patient_user = User.query.filter_by(user_id = user_id).first_or_404()
    patient = Patient.query.filter_by(user_id = user_id).first_or_404()
    prescription = Prescription.query.filter_by(patient_id = user_id).order_by(Prescription.prescription_id.desc()).all()
    health_check = Health_check.query.filter_by(patient_id = user_id).order_by(Health_check.record_id.desc()).all()

    if request.form.get('active'):
        prescription_id = int(request.form['active'][:-1])
        status = int(request.form['active'][-1])
        target_prescript = Prescription.query.filter_by(prescription_id = prescription_id).first()
        target_prescript.active = int(request.form['active'][-1])
        db.session.commit()
        flash("Update Succesful")
        session["Patient_ID"] = user_id
        return redirect(url_for('profile.search'))

    if request.form.get('notify'):
        prescription_id = int(request.form['notify'][:-1])
        status = int(request.form['notify'][-1])
        target_prescript = Prescription.query.filter_by(prescription_id = prescription_id).first()
        print(status)
        target_prescript.notify = int(request.form['notify'][-1])
        db.session.commit()
        flash("Update Succesful")
        session["Patient_ID"] = user_id
        return redirect(url_for('profile.search'))
    return render_template('profile/search_patient_alt.html', patient_user = patient_user, patient = patient, prescription = prescription, health_check = health_check)



#<a href="{{ url_for('profile.patient', user_id=selected_id) }}">Confirm Selection</a>
@profile.route('/autocomplete', methods = ['GET', 'POST'])
@login_required
def autocomplete():
    if request.method == 'GET':
        search = request.args.get('q')
        if search == None:
            search = ""
        #.filter_by(role_id = Role.query(Role.id).filter_by(name = "Patient"))
        query = db.session.query(User.first_name, User.last_name, User.user_id).filter_by(hospital_id = current_user.hospital_id).filter(User.last_name.like('%' + str(search) + '%'))
        results = [[i[0] + " " + i[1], i[2]] for i in query.all()]
        return jsonify(matching_results = results)
    else:
        session["Patient_ID"] = int(request.get_json())
        return render_template('profile/search_patient.html')

@profile.route("/patient")
@login_required
def patient():
    user_id = current_user.user_id
    patient_user = User.query.filter_by(user_id = user_id).first_or_404()
    patient = Patient.query.filter_by(user_id = user_id).first_or_404()
    prescription = Prescription.query.filter_by(patient_id = user_id).order_by(Prescription.prescription_id.desc()).all()
    health_check = Health_check.query.filter_by(patient_id = user_id).order_by(Health_check.record_id.desc()).all()
    if request.form.get('notify'):
        prescription_id = int(request.form['notify'][:-1])
        status = int(request.form['notify'][-1])
        target_prescript = Prescription.query.filter_by(prescription_id = prescription_id).first()
        target_prescript.notify = int(request.form['notify'][-1])
        db.session.commit()
        flash("Update Succesful")
        return redirect(url_for('profile.patient'))
    return render_template('profile/patient.html', patient_user = patient_user, patient = patient, prescription = prescription, health_check = health_check)


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
