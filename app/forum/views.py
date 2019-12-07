from flask import render_template, redirect, request, url_for, flash, current_app
from . import forum
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

@forum.route('/home',  methods = ['GET','POST'])
@login_required
def home():
    update_forum()
    update_posts()
    top_forums = Top_forums.query.join(Forum, (Top_forums.forum_id == Forum.forum_id)).all()
    top_posts = Top_posts.query.join(Post, (Top_posts.post_id == Post.post_id)).all()
    return render_template('forum/home.html', top_forums = top_forums, top_posts = top_posts)

def update_forum():
    update_f_task = Task.query.filter(Task.name == "update_forum").first()
    print(update_f_task)
    if update_f_task:
        if update_f_task.time_requested < datetime.utcnow() - relativedelta(hours = 24):
            current_user.launch_task(name = 'update_forum', description = 'Updating Top Forums')
    else:
        current_user.launch_task(name = 'update_forum', description = 'Updating Top Forums')
        print('adding_task')
    db.session.commit()

def update_posts():
    update_p_task = Task.query.filter(Task.name == "update_posts").first()
    print(update_p_task)
    if update_p_task:
        if update_p_task.time_requested < datetime.utcnow() - relativedelta(minutes = 1):
            current_user.launch_task(name = 'update_posts', description = 'Updating Top Posts')
    else:
        current_user.launch_task(name = 'update_posts', description = 'Updating Top Posts')
        print('adding_task')
    db.session.commit()

@forum.route('/forums', methods = ['GET', 'POST'])
def forums():
    return 
