from flask import render_template, redirect, request, url_for, flash
from .forms import NewStaffForm
from datetime import datetime, date
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Physician, Nurse, User
from .. import db
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
        session["Staff_ID"] = int(request.get_json())
        return render_template('admin_tools/search_staff.html')
