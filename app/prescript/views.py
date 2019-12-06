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
    form = NewPrescriptionForm()
    print(form)
    if form.validate_on_submit():
        #search = request.args.get('search')
        #result = User.Query(user).filter(full_name.like('%' + search + '%')).all()
        prescription = Prescription(
                    patient_id = session["Patient_ID"],
                    physican_id = current_user.user_id,
                    date_prescribed = datetime.utcnow(),
                    expire_date = form.expire_date.data,
                    description = form.description.data)
        db.session.add(prescription)
        print(prescription)
        db.session.commit()
        flash('New Prescription Created.')
        session.pop("Patient_ID")
        #Need to figure out form formatting for where to throw each patient
    return render_template('prescript/new_prescription.html', form = form)

@prescript.route('/view_prescriptions', methods = ['GET', 'POST'])
@login_required
def view_prescriptions():
    active_prescriptions = Prescription.Query(patient_id = current_user.user_id).all()
    return render_template('prescript/view_prescription.html', data = active_prescriptions)
