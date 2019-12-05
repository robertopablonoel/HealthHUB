from flask import render_template, redirect, request, url_for, flash
from . import forum
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Patient, User, Physician
from .forms import *
from .. import db
import re

@forum.route('/home', methods = ['GET','POST'])
@login_required
def home():
    return render_template("/forum/forum_home.html")
#Here comes the scheduling code...

#Here comes the scheduling code...
'''
hospitals = Hospital.query.all()
form = PatientRegistrationForm()
'''