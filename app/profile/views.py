from flask import render_template, redirect, request, url_for, flash
from .forms import ModifyPrescriptionForm
from datetime import datetime, date
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Prescription, User, Patient
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
    prescription = Prescription.query.filter_by(patient_id = user_id).all()

    if request.form.get('active'):
        prescription_id = int(request.form['active'][:-1])
        status = int(request.form['active'][-1])
        target_prescript = Prescription.query.filter_by(prescription_id = prescription_id).first()
        target_prescript.active = int(request.form['active'][-1])
        db.session.commit()
        flash("Update Succesful")
        session["Patient_ID"] = user_id
        print("this")
        print(session.get("Patient_ID"))
        print("one")
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
    return render_template('profile/search_patient_alt.html', patient_user = patient_user, patient = patient, prescription = prescription)



#<a href="{{ url_for('profile.patient', user_id=selected_id) }}">Confirm Selection</a>
@profile.route('/autocomplete', methods = ['GET', 'POST'])
@login_required
def autocomplete():
    if request.method == 'GET':
        search = request.args.get('q')
        if search == None:
            search = ""
        query = db.session.query(User.last_name, User.user_id).filter(User.last_name.like('%' + str(search) + '%'))
        results = [[i[0], i[1]] for i in query.all()]
        print(results)
        return jsonify(matching_results = results)
    else:
        session["Patient_ID"] = int(request.get_json())
        print(session["Patient_ID"])
        return render_template('profile/search_patient.html')
