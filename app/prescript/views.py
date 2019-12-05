from flask import render_template, redirect, request, url_for, flash
from .forms import NewPrescriptionForm
from datetime import datetime, date
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Prescription, User
from .. import db
from . import prescript
from flask_jsonpify import jsonify
import re


@prescript.route('/new_prescription', methods = ['GET','POST'])
@login_required
def new_prescription():
    """
    form = NewPrescriptionForm()
    if form.validate_on_submit():
        #search = request.args.get('search')
        #result = User.Query(user).filter(full_name.like('%' + search + '%')).all()
        prescription = Prescription(
                    physican_id = current_user.user_id,
                    date_prescribed = datetime.utcnow(),
                    expire_date = form.expire_date.data,
                    description = form.description.data)
        db.session.add(prescription)
        print(prescription)
        db.session.commit()
        flash('New Prescription Created.')
        #Need to figure out form formatting for where to throw each patient
    return render_template('prescript/new_prescription.html', form = form)
    """
    return render_template('prescript/search_patient.html')

@prescript.route('/view_prescriptions', methods = ['GET', 'POST'])
@login_required
def view_prescriptions():
    active_prescriptions = Prescription.Query(patient_id = current_user.user_id).all()
    return render_template('prescript/view_prescription.html', data = active_prescriptions)

@prescript.route('/autocomplete', methods = ['GET'])
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
