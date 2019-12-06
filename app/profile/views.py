from flask import render_template, redirect, request, url_for, flash
from .forms import NewPrescriptionForm
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
    print("yo yo you got ya bo")
    user_id = session["Patient_ID"]
    patient_user = User.query.filter_by(user_id = user_id).first_or_404()
    patient = Patient.query.filter_by(user_id = user_id).first_or_404()
    prescription = Prescription.query.filter_by(patient_id = user_id).all()

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
