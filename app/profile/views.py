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


@profile.route('/patient', methods = ['GET','POST'])
@login_required
def patient():
    if Patient.query.filter_by(user_id = current_user.user_id).first() == True:
        user_id = current_user.user_id
        patient_user = current_user
    else:
        user_id = session["Patient_ID"]
        patient_user = User.query.filter_by(user_id = user_id).first_or_404()
    patient = Patient.query.filter_by(user_id = user_id).first_or_404()
    prescription = Prescription.query.filter_by(patient_id = user_id).all()
    if request.form.get('active'):
        prescription_id = int(request.form['active'][:-1])
        target_prescript = Prescription.query.filter_by(prescription_id = prescription_id)
        print(target_prescript)
        target_prescript.active = int(request.form['active'][-1])
        print(target_prescript)
        db.session.commit()
        flash("Update Succesful")
        return redirect(url_for('profile.patient'))
    if request.form.get('notify'):
        print('ding this is a Notify')

    return render_template('profile/patient.html', patient_user = patient_user, patient = patient, prescription = prescription)

@profile.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
    return render_template('profile/search_patient.html')

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



@profile.route('/modify_prescript/<prescription_id>', methods = ['GET', 'POST'])
@login_required
def modify_prescript(prescription_id):
    form = ModifyPrescriptionForm()
    target_prescript = Prescription.query.filter_by(prescription_id = prescription_id)
    #form.active.default = target_prescript.active
    #form.notification.default = target_prescript.notify
    if form:
        print(target_prescript)
        copy = target_prescript
        target_prescript.active = form.active.data
        target_prescript.notify = form.notify.data
        if copy != target_prescript:
            print("Updated:", target_prescript)
            db.session.commit()
            flash("Prescription Updated Sucessfully")

    return render_template('profile/modify_prescript.html', form = form )
