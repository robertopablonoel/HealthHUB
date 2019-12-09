from flask import render_template, redirect, request, url_for, flash
from datetime import datetime, date
from flask_login import login_user, login_required, logout_user, current_user
from ... import db
from . import files_uploaded
from flask_jsonpify import jsonify
from flask import session
import os
import re

@files_uploaded.route('/<pdf_name>' , methods = ["GET", "POST"])
@login_required
def view_pdf(pdf_name):
    print("We got the viewing pdf")
    UPLOAD_FOLDER = "app/templates/"
    USER_FOLDER = str(current_user.user_id)

    return render_template("files_uploaded/files.html", pdf_name = pdf_name, user_folder = USER_FOLDER)
