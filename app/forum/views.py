from flask import render_template, redirect, request, url_for, flash, current_app
from . import forum
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Permission, Patient, User, Hospital, Forum, Forum_members, ForumPermission, Post, Likes, Reaction, Top_forums, Top_posts
from ..email import send_email
from .. import db, scheduler
from ..decorators import permission_required
from datetime import date
import re
# from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from flask import Flask

@forum.route('/home', methods = ['GET', 'POST'])
def home():
    return render_template("/forum/forum_home.html")
@forum.route('/get_top_tables', methods = ['GET', 'POST'])
# @login_required
# @permission_required(Permission.ADMINISTRATOR)
def get_top_tables():
    scheduler.add_job(func=update_tables, trigger = 'interval',seconds=8, id="1")

app=scheduler.app
with app.app_context():
    def update_tables():
        top_forums = Forum.query.join(Forum_members, (Forum.forum_id == Forum_members.forum_id)) \
                                .with_entities(Forum.hospital_id, Forum.forum_id, Forum.db.func.count(Forum_members.user_id)) \
                                .group_by(Forum.hospital_id, Forum.forum_id).order_by(Forum.db.func.count(Forum_members.user_id).desc()).all()[:5]
        print(top_forums)

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
