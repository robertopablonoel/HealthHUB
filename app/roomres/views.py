from flask import render_template, redirect, request, url_for, flash
from . import roomres
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Patient, User, Physician
from .forms import viewRooms
from .. import db
from ..decorators import permission_required
import re

@roomres.route('/reserve', methods = ['GET','POST'])
@permission_required(Permission.BOOK_ROOMS)
def reserve():
    full_rooms = [i for i in range(0,1000,2)]
    all_rooms = [i for i in range(0,1000)]
    physicians = User.query.join(Physician).all()
    form = viewRooms()
    form.physician.choices = [(p.user_id, p.first_name + " " + p.last_name) for p in physicians]
    print(form.physician.choices)
    '''
    if form.validate_on_submit():
        print(form.hospital.data)
        user = User(email = form.email.data,
                    password = form.password.data,
                    first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    hospital_id = form.hospital.data)
        db.session.add(user)
        print(user)
        db.session.commit()
        print(user)
        patient = Patient(date_of_birth = form.date_of_birth.data, user = user)
        db.session.add(patient)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                     'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    '''
    return render_template("/roombooking/room_booking.html", form = form, full_rooms = full_rooms, all_rooms = all_rooms)
#Here comes the scheduling code...

#Here comes the scheduling code...
'''
hospitals = Hospital.query.all()
form = PatientRegistrationForm()
'''
