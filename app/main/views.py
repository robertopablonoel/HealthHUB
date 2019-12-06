from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .. import db
from ..auth.forms import LoginForm

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from ..models import User

@main.route('/', methods = ['GET','POST'])
def index():
    return render_template('index.html')

@main.route('/home', methods = ['GET','POST'])
@login_required
def home():
    return render_template('home.html')
