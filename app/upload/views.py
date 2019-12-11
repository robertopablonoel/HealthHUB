from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import os, sys
from flask import render_template, redirect, request, url_for, flash, current_app, session
from . import upload
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Permission, Patient, User, Hospital, Forum, Forum_members, ForumPermission, Post, Likes, Reaction, Top_forums, Top_posts, Task
from ..email import send_email
from .. import db
from ..decorators import permission_required
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
from flask import Flask
# Upload files routing
@upload.route("/uploads", methods=['GET','POST'])
@login_required
def uploads():
    print(os.getcwd())
    UPLOAD_FOLDER = "app/templates/files_uploaded/"
    USER_FOLDER = str(session.get("Patient_ID"))
    try:
        files=os.listdir(os.path.join(UPLOAD_FOLDER, USER_FOLDER))
        print(files)
    except FileNotFoundError:
        files = []

    return render_template("upload/file_upload.html", files=files)

@upload.route("/uploader", methods=['GET','POST'])
@login_required
def uploader():
    print('arrived')
    file_exists = False
    UPLOAD_FOLDER = "app/templates/files_uploaded/"
    USER_FOLDER = str(session.get("Patient_ID"))
    if request.method == "POST":
        print("Request Files", request.files)
        f = request.files['file']

        file = secure_filename(f.filename)
        try:
            files = os.listdir(os.path.join(UPLOAD_FOLDER, USER_FOLDER))
            if file in files:
                raise FileExistsError("File Already Exists, the file will not be saved")
            else:
                f.save(os.path.join(UPLOAD_FOLDER, USER_FOLDER, file))
                return redirect(url_for("upload.uploader"))
        except FileExistsError:
            file_exists = True
        except FileNotFoundError:
             os.mkdir(os.path.join(UPLOAD_FOLDER,USER_FOLDER))
             f.save(os.path.join(UPLOAD_FOLDER, USER_FOLDER, file))
             return redirect(url_for("upload.uploader"))
    files = os.listdir(os.path.join(UPLOAD_FOLDER, USER_FOLDER))
        #try:
        #    f.save(os.path.join(UPLOAD_FOLDER, USER_FOLDER, secure_filename(f.filename)))
        #except FileNotFoundError:
    #        print("Encountered a FileNotFoundError, creating a file >>> ", USER_FOLDER)
        #    os.mkdir(os.path.join(UPLOAD_FOLDER, USER_FOLDER))
    #        f.save(os.path.join(UPLOAD_FOLDER, USER_FOLDER, secure_filename(f.filename)))
        # print(os.getcwd())
        # print(os.path.join(UPLOAD_FOLDER, USER_FOLDER))
        # f.save(os.path.join(UPLOAD_FOLDER,USER_FOLDER,secure_filename(f.filename)))
        #files=os.listdir(os.path.join(UPLOAD_FOLDER, USER_FOLDER))
    return render_template("upload/file_upload.html", files=files, file_exists = file_exists)

@upload.route("/file_viewer")
@login_required
def view_file():
    return render_template("upload/file_viewer.html")
