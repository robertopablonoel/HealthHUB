from flask import render_template, redirect, request, url_for, flash
from .forms import NewPrescriptionForm
from datetime import datetime, date
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Prescription, User, Patient
from .. import db
from . import profile
from flask_jsonpify import jsonify
import re


@profile.route('/patient/<user_id>', methods = ['GET','POST'])
@login_required
def patient(user_id):
    print("yo yo you got ya boi")
    patient_user = User.query.filter_by(user_id = user_id).first_or_404()
    patient = Patient.query.filter_by(user_id = user_id).first_or_404()
    precription = Prescription.query.filter_by(patient_id = user_id).all()
    return render_template('profile/patient.html', patient_user = patient_user, patient = patient, prescription = prescription)

@profile.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
    return render_template('profile/search_patient.html')

@profile.route('/autocomplete', methods = ['GET'])
@login_required
def autocomplete():
    search = request.args.get('q')
    print("got the search it is :")
    print(search)
    if search == None:
        search = ""
    query = db.session.query(User.last_name, User.user_id).filter(User.last_name.like('%' + str(search) + '%'))
    results = [i[0] for i in query.all()]
    return jsonify(matching_results = results)
