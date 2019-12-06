from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import os
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

UPLOAD_FOLDER = "./files_uploaded/"

@upload.route("/uploads")
def uploads():
    return render_template("file_upload.html")

@upload.route("/uploader", methods=['GET','POST'])
def upload_file():
    if request.method == "POST":
        print("Request Files", request.files)
        f = request.files('file')
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        return('File uplaoded successfully')
