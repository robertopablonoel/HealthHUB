from flask import render_template, redirect, request, url_for, flash
from .forms import NewStaffForm
from datetime import datetime, date
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Physician, Nurse, User, Permission
from .. import db
from ..decorators import permission_required
from . import admin_tools
from flask_jsonpify import jsonify
from flask import session
import re

@admin_tools.route('/register_staff', methods = ['GET', 'POST'])
def register_staff():
    hospitals = Hospital.query.all()
    form = NewStaffForm()
    form.hospital.choices = [(h.unique_id, h.name) for h in hospitals]
    print(form.hospital.choices)
    if form.validate_on_submit():
        print(form.hospital.data)
        user = User(email = form.email.data,
                    password = form.password.data,
                    first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    hospital_id = form.hospital.data,
                    role_id = form.roll.data)
        db.session.add(user)
        db.session.commit()
        if form.roll.data == 6:
            new_staff = Physician(
                    user_id = user.user_id
            )
        if form.roll.data == 7:
            new_staff = Nurse(
                    user_id = user.user_id
            )
        db.session.add(new_staff)
        db.session.commit()
        print(user)
        flash('A New Staff Member as been added')
        return redirect(url_for('admin_tools.search'))
    return render_template('admin_tools/register_staff.html', form = form)


@admin_tools.route('/set_search')
@login_required
def set_search():
    if session.get("Staff_ID") != None:
        session.pop("Staff_ID")
    return redirect(url_for('admin_tools.search'))

@admin_tools.route('/search', methods = ['GET', 'POST'])
@login_required
@permission_required(Permission.SEARCH_PATIENT)
def search():
    print(session.get("Staff_ID"))
    if session.get("Staff_ID") == None:
        return render_template('admin_tools/search_staff.html')
    user_id = session.get("Staff_ID")
    staff_user = User.query.filter_by(user_id = user_id).first_or_404()
    if staff_user.role_id == 6:
        staff = Physician.query.filter_by(user_id = user_id).first_or_404()
    if staff_user.role_id == 7:
        staff = Nurse.query.filter_by(user_id = user_id).first_or_404()

    if request.form.get('active'):
        status = int(request.form['active'][-1])
        staff_user.active = status
        db.session.commit()
        flash("Update Succesful")

        return redirect(url_for('admin_tools.search'))

    return render_template('admin_tools/search_staff_alt.html', staff_user = staff_user)



#<a href="{{ url_for('profile.patient', user_id=selected_id) }}">Confirm Selection</a>
@admin_tools.route('/autocomplete', methods = ['GET', 'POST'])
@login_required
@permission_required(Permission.SEARCH_PATIENT)
def autocomplete():
    if request.method == 'GET':
        search = request.args.get('q')
        if search == None:
            search = ""
        #.filter_by(role_id = Role.query(Role.id).filter_by(name = "Patient"))
        query = db.session.query(User.first_name, User.last_name, User.user_id, User.role_id).filter_by(hospital_id = current_user.hospital_id).filter(User.last_name.like('%' + str(search) + '%'))
        rd = {6: "Physician", 7: "Nurse"}
        results = [[rd[i[3]] + " : " + i[0] + " " + i[1], i[2]] for i in query.all()]
        return jsonify(matching_results = results)
    else:
# <<<<<<< HEAD
        session["Staff_ID"] = int(request.get_json())
        return render_template('admin_tools/search_staff.html')
# =======
#
#         session["Staff_ID"] = int(request.get_json())
#         return render_template('admin_tools/search_staff.html')
# ''''
# >>>>>>> ae6654c74a358cf3368f4d091da86ec7c1cb1451
#         session["Patient_ID"] = int(request.get_json())
#         return render_template('profile/search_patient.html')
#         '''

@admin_tools.route("/patient")
@login_required
@permission_required(Permission.UPDATE_NOTIFICATIONS)
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


@admin_tools.route('/new_health_check', methods = ['GET','POST'])
@permission_required(Permission.ADD_CHECKUP)
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
