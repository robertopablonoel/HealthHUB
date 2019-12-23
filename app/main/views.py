from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .. import db
from ..auth.forms import LoginForm

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from ..models import User, Post, Likes, Forum_profile, Top_posts

@main.route('/', methods = ['GET','POST'])
def index():
    return render_template('index.html')

@main.route('/home', methods = ['GET','POST'])
@login_required
def home():
    top_p = db.session.query(Top_posts, Post, Likes, Forum_profile) \
                            .join(Post, Top_posts.post_id == Post.post_id) \
                            .outerjoin(Likes, (Post.post_id == Likes.post_id)) \
                            .join(Forum_profile, (Forum_profile.user_id == Post.user_id)) \
                            .with_entities(Post.forum_id, Post.post_id, Post.content, Forum_profile.username,Top_posts.forum_name, db.func.count(Likes.user_id).label("count_likes")) \
                            .group_by(Post.post_id, Top_posts.forum_name).order_by(Post.date_posted.desc()).all()
    return render_template('home.html', top_p = top_p)

@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'
