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

<<<<<<< HEAD
@forum.route('/forums',  methods = ['GET','POST'])
@login_required
def forums():
    update_forum()
    update_posts()
    top_forums = Top_forums.query.join(Forum, (Top_forums.forum_id == Forum.forum_id)).all()
    top_posts = Top_posts.query.join(Post, (Top_posts.post_id == Post.post_id)).all()
    return render_template('forum/forum.html', top_forums = top_forums, top_posts = top_posts)

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
=======
@forum.route('/home', methods = ['GET', 'POST'])
def home():
    return render_template("/forum/forum_home.html")
@forum.route('/get_top_tables', methods = ['GET', 'POST'])
# @login_required
# @permission_required(Permission.ADMINISTRATOR)
def get_top_tables():
    scheduler.add_job(func=update_tables, trigger = 'interval',seconds=8, id="1")
>>>>>>> 00dc6361c5b5dcbb17a25bcf0604623a46dd052f

@forum.route('/home', methods = ['GET', 'POST'])
def home():
    return render_template('forum/home.html')

@forum.route('/whatever', methods = ['GET','POST'])
@login_required
# @permission_required('')
def whatever():
    current_user.hospital_id
    #Subquery to get all forums that user is a part of
    user_forums = Forum_members.query.filter(Forum_members.user_id == current_user.user_id).subquery()
    reactions = Post.query.join(Likes, (Post.post_id == Likes.post_id)).join(Reaction, (Post.post_id == Reaction.post_id)).subquery()

    print(reactions)
    return
