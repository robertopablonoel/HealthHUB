from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import os, sys
from flask import render_template, redirect, request, url_for, flash, current_app
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

UPLOAD_FOLDER = "app/templates/files_uploaded/"
USER_FOLDER = "files/"
@upload.route("/uploads", methods=['GET','POST'])
@login_required
def uploads():
    files=os.listdir(os.path.join(UPLOAD_FOLDER, USER_FOLDER))
    print(files)
    return render_template("upload/file_upload.html", files=files)

@upload.route("/uploader", methods=['GET','POST'])
@login_required
def uploader():
    print('arrived')
    if request.method == "POST":
        print("Request Files", request.files)
        f = request.files['file']
        try:
            f.save(os.path.join(UPLOAD_FOLDER, USER_FOLDER, secure_filename(f.filename)))
        except FileNotFoundError:
            print("Encountered a FileNotFoundError, creating a file >>> ", USER_FOLDER)
            os.mkdir(os.path.join(UPLOAD_FOLDER, USER_FOLDER))
            f.save(os.path.join(UPLOAD_FOLDER, USER_FOLDER, secure_filename(f.filename)))
        # print(os.getcwd())
        # print(os.path.join(UPLOAD_FOLDER, USER_FOLDER))
        # f.save(os.path.join(UPLOAD_FOLDER,USER_FOLDER,secure_filename(f.filename)))
        files=os.listdir(os.path.join(UPLOAD_FOLDER, USER_FOLDER))
        return render_template("upload/file_upload.html", files=files)

@upload.route("/file_viewer")
@login_required
def view_file():
    return render_template("upload/file_viewer.html")
