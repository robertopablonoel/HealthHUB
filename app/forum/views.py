from flask import render_template, redirect, request, url_for, flash, current_app, session
from . import forum
from flask_login import login_user, login_required, logout_user, current_user
from ..models import Permission, Patient, User, Hospital, Forum, Forum_role, Forum_members, ForumPermission, Post, Likes, Reaction, Top_forums, Top_posts, Task, Forum_profile, Forum_role
from ..email import send_email
from .. import db
from ..decorators import permission_required
from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .forms import PostForm, createForumForm, editBio
import re
from flask import Flask
from flask_jsonpify import jsonify
from os import path
import os

@forum.route('/home',  methods = ['GET','POST'])
@login_required
def home():
    update_forum()
    update_posts()

    top_f = db.session.query(Top_forums, Forum).join(Forum, (Top_forums.forum_id == Forum.forum_id)).filter(Top_forums.forum_id == Forum.forum_id).order_by(Top_forums.subscribers.desc()).limit(8).all()
    top_p = db.session.query(Top_posts, Post, Likes, Forum_profile) \
                            .join(Post, Top_posts.post_id == Post.post_id) \
                            .outerjoin(Likes, (Post.post_id == Likes.post_id)) \
                            .join(Forum_profile, (Forum_profile.user_id == Post.user_id)) \
                            .with_entities(Post.forum_id, Post.post_id, Post.content, Forum_profile.username,Top_posts.forum_name, db.func.count(Likes.user_id).label("count_likes")) \
                            .group_by(Post.post_id, Top_posts.forum_name).order_by(Post.date_posted.desc()).all()
    if request.method == "POST":
        if request.values.get('like'):
            like(request.values.get('like'))
            flash("liked!")
            return redirect(url_for('forum.home'))
        elif request.values.get('unlike'):
            unlike(request.values.get('unlike'))
            flash("unliked :(")
            return redirect(url_for('forum.home'))

    filepath = '/Users/robertonoel/Desktop/EHR/app/templates/files_uploaded/profile/' + str(current_user.user_id) + '/icon.png'
    has_icon = path.exists(filepath)
    print(filepath)
    print(has_icon)
    forum_pro = Forum_profile.query.filter(Forum_profile.user_id == current_user.user_id).first()
    user_forums = db.session.query(Forum_members, Forum).join(Forum, Forum_members.forum_id == Forum.forum_id).filter(Forum_members.user_id == current_user.user_id).all()
    return render_template('forum/home.html', top_f = top_f, top_p = top_p, forum_pro = forum_pro, user_forums = user_forums, has_icon = has_icon)

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


@forum.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    #Returns recent comments, recent posts, recent likes, bio_link,
    posted_posts = Post.query.filter(Post.user_id == current_user.user_id).order_by(Post.date_posted.desc()).all()
    liked_posts = Likes.query.join(Post, (Likes.post_id == Post.post_id)).filter(Likes.user_id == current_user.user_id) \
                                .order_by(Likes.date_liked.desc()).all()
    reaction_posts = Reaction.query.join(Post, (Reaction.post_id == Post.post_id)).filter(Reaction.user_id == current_user.user_id) \
                                    .order_by(Reaction.date_commented.desc()).all()
    user_attributes = User.query.filter(User.user_id == current_user.user_id).first()
    forum_pro = Forum_profile.query.filter(Forum_profile.user_id == current_user.user_id)
    #In order to access profile, you need to href for images, which will be a static path
    if request.method == "Post":
        if request.form.get('new_bio'):
            new_bio = request.form['new_bio']
            profile = Forum_profile.query.filter(Forum.user_id == current_user.user_id).first()
            profile.bio = new_bio
            db.session.commit()
        elif request.files['file']:
            profile_upload(request, current_user.user_id)
        return render_template('forum/profile.html', posted_posts = posted_posts, liked_posts = liked_posts, reaction_posts = reaction_posts, user_attributes = user_attributes, forum_pro = forum_pro)
    return render_template('forum/profile.html', posted_posts = posted_posts, liked_posts = liked_posts, reaction_posts = reaction_posts, user_attributes = user_attributes, forum_pro = forum_pro)

def profile_upload(req, user_id):
    UPLOAD_FOLDER = "app/templates/files_uploaded/"
    USER_FOLDER = "profile/{}/".format(user_id)
    print("Request Files", request.files)
    f = req.files['file']
    try:
        f.save(os.path.join(UPLOAD_FOLDER, USER_FOLDER, secure_filename("icon.png")))
    except FileNotFoundError:
        print("Encountered a FileNotFoundError, creating a file >>> ", USER_FOLDER)
        os.mkdir(os.path.join(UPLOAD_FOLDER, USER_FOLDER))
        f.save(os.path.join(UPLOAD_FOLDER, USER_FOLDER, secure_filename("icon.png")))
    files=os.listdir(os.path.join(UPLOAD_FOLDER, USER_FOLDER))

@forum.route('/mini_direct')
def mini_direct():
    print(session.get("forum_name"))
    return redirect(url_for("forum.page", forum_name= session.get("forum_name")))

@forum.route('/hh/<forum_name>', methods = ['GET', 'POST'])
def page(forum_name):
    curr_forum = Forum.query.filter(Forum.forum_name == forum_name).first()
    form = PostForm()
    tot_likes = len(db.session.query(Post, Likes).filter(Post.forum_id == curr_forum.forum_id).outerjoin(Likes, (Post.post_id == Likes.post_id)).all())
    if curr_forum:
        forum_members = Forum_members.query.filter(Forum_members.forum_id == curr_forum.forum_id).all()
        # Sub_query = Likes.query.with_entities((Likes.post_id), db.func.count(Likes.user_id)).group_by(Likes.post_id).subquery()
        forum_posts = db.session.query(Post, Likes, Forum_profile) \
                                .filter(Post.forum_id == curr_forum.forum_id) \
                                .outerjoin(Likes, (Post.post_id == Likes.post_id)) \
                                .join(Forum_profile, (Forum_profile.user_id == Post.user_id)) \
                                .with_entities(Post.forum_id, Post.post_id, Post.content, Forum_profile.username, db.func.count(Likes.user_id).label("count_likes")) \
                                .group_by(Post.post_id).order_by(Post.date_posted.desc()).all()
        subscribed = get_subscribed(forum_members)
        if request.method == "POST":
            if request.values.get('submit') == 'subscribe':
                print('subscribe')
                subscribed = add_subscription(curr_forum)
                flash('You have successfully subscribed.')
                return redirect(url_for('forum.page', forum_name = forum_name))
            elif request.values.get('submit') == 'unsubscribe':
                print('unsubscribe')
                Forum_members.query.filter((Forum_members.forum_id == curr_forum.forum_id) & (Forum_members.user_id == current_user.user_id)).delete()
                db.session.commit()
                subscribed = False
                flash('You have been successfully unsubscribed.')
                return redirect(url_for('forum.home'))
            elif request.values.get('like'):
                like(request.values.get('like'))
                flash("liked!")
                return redirect(url_for('forum.page', forum_name = forum_name))
            elif request.values.get('unlike'):
                unlike(request.values.get('unlike'))
                flash("unliked :(")
                return redirect(url_for('forum.page', forum_name = forum_name))
        if form.validate_on_submit():
            try:
                add_post(form.text.data, curr_forum)
                flash('Post Submitted')
                return redirect(url_for('forum.page', forum_name = forum_name))
            except:
                flash('Post Failed to Submit')
                return redirect(url_for('forum.page', forum_name = forum_name))
        else:
            return render_template('forum/page.html', form = form, curr_forum = curr_forum, forum_members = forum_members, forum_posts = forum_posts, subscribed = subscribed, tot_likes = tot_likes)
    else:
        flash('Invalid Forum Route')
        return redirect(url_for('forum.home'))

def like(post_id):
    new_like = Likes(post_id = post_id,
                        user_id = current_user.user_id,
                        date_liked = datetime.now())
    db.session.add(new_like)
    db.session.commit()

def unlike(post_id):
    Likes.query.filter((Likes.post_id == post_id) & (Likes.user_id == current_user.user_id)).delete()
    db.session.commit()

def get_subscribed(forum_members):
    if current_user.user_id in [i.user_id for i in forum_members]:
        return True
    else:
        return False

def add_post(text, curr_forum):
    new_post = Post(forum_id = curr_forum.forum_id,
                    date_posted = datetime.now(),
                    user_id = current_user.user_id,
                    content = text)
    db.session.add(new_post)
    db.session.commit()

def add_subscription(curr_forum):
    subscription = Forum_members(forum_id = curr_forum.forum_id,
                                user_id = current_user.user_id,
                                role_id = Forum_role.query.filter_by(default = True).first().id)
    db.session.add(subscription)
    db.session.commit()
    return True



@forum.route('/hh/<forum_name>/<post_id>', methods = ["GET", "POST"])
def page_post(forum_name, post_id):
    curr_forum = Forum.query.filter(Forum.forum_name == forum_name).first()
    curr_post = db.session.query(Post, Forum_profile).filter(Post.post_id == post_id).join(Forum_profile, (Forum_profile.user_id == Post.user_id)).first()
    curr_comments = db.session.query(Reaction, Forum_profile).join(Forum_profile, (Forum_profile.user_id == Reaction.user_id)).filter(Reaction.post_id == post_id).order_by(Reaction.date_commented.asc())
    count_likes = Likes.query.filter(Likes.post_id == post_id) \
                            .with_entities(Likes.post_id, db.func.count(Likes.user_id)) \
                            .group_by(Likes.post_id).first()[1]
    tot_posts = len(Post.query.filter(Post.forum_id == curr_forum.forum_id).all())
    tot_likes = len(db.session.query(Post, Likes).filter(Post.forum_id == curr_forum.forum_id).outerjoin(Likes, (Post.post_id == Likes.post_id)).all())
    form = PostForm()
    if curr_forum and curr_post:
        forum_members = Forum_members.query.filter(Forum_members.forum_id == curr_forum.forum_id).all()
        subscribed = get_subscribed(forum_members)
        if request.method == "POST":
            print([i for i in request.form.keys()])
            print(request.form['submit'])
            if request.values.get('submit') == 'subscribe':
                print('subscribe')
                subscribed = add_subscription(curr_forum)
                flash('You have successfully subscribed.')
                return redirect(url_for('forum.page_post', forum_name = forum_name, post_id = post_id))
            elif request.values.get('submit') == 'unsubscribe':
                print('unsubscribe')
                Forum_members.query.filter((Forum_members.forum_id == curr_forum.forum_id) & (Forum_members.user_id == current_user.user_id)).delete()
                db.session.commit()
                subscribed = False
                flash('You have been successfully unsubscribed.')
                return redirect(url_for('forum.home'))
            elif request.values.get('like'):
                try:
                    like(request.values.get('like'))
                    flash("liked!")
                    return redirect(url_for('forum.page_post', forum_name = forum_name, post_id = post_id))
                except:
                    return redirect(url_for('forum.page_post', forum_name = forum_name, post_id = post_id))
            elif request.values.get('unlike'):
                try:
                    unlike(request.values.get('unlike'))
                    flash("unliked :(")
                    return redirect(url_for('forum.page_post', forum_name = forum_name, post_id = post_id))
                except:
                    return redirect(url_for('forum.page_post', forum_name = forum_name, post_id = post_id))
        if form.validate_on_submit():
            try:
                add_comment(form.text.data, curr_post)
                flash('Comment Added')
                return redirect(url_for('forum.page_post', forum_name = forum_name, post_id = post_id))
            except:
                flash('Comment Failed to Submit')
                return redirect(url_for('forum.page_post', forum_name = forum_name, post_id = post_id))
        else:
            return render_template('forum/page_post.html', form = form, curr_forum = curr_forum, curr_post = curr_post, curr_comments = curr_comments, count_likes = count_likes, forum_members = forum_members, subscribed = subscribed, tot_likes = tot_likes, tot_posts = tot_posts)
    else:
        flash('Invalid Forum Route')
        return redirect(url_for('forum.home'))

def add_comment(text, curr_post):
    new_comment = Reaction(post_id = curr_post[0].post_id,
                    user_id = current_user.user_id,
                    comment = text,
                    date_commented = datetime.now())
    db.session.add(new_comment)
    db.session.commit()

@forum.route('/create', methods = ["GET", "POST"])
def create():
    form = createForumForm()
    if form.validate_on_submit():
        try:
            createForum(form)
            return redirect(url_for('forum.page', forum_name = form.title.data))
        except:
            flash("Error Creating Forum")
            return redirect(url_for('forum.home'))
    return render_template('forum/create.html', form = form)

def createForum(form):
    new_forum = Forum(forum_name = form.title.data,
                        hospital_id = current_user.hospital_id,
                        description = form.text.data,
                        public = 1 if form.visibility.data == 1 else 0,
                    )
    db.session.add(new_forum)
    db.session.commit()


@forum.route('/autocomplete', methods = ['GET', 'POST'])
@login_required
def autocomplete():
    session["forum_name"] = ""
    if request.method == 'GET':
        search = request.args.get('q')
        if search == None:
            search = ""
        #.filter_by(role_id = Role.query(Role.id).filter_by(name = "Patient"))
        query = db.session.query(Forum.forum_name).filter(Forum.forum_name.like('%' + str(search) + '%'))
        #.filter_by(hospital_id = current_user.hospital_id)
        results = [[i[0]] for i in query.all()]
        return jsonify(matching_results = results)
    else:
        print("help")
        session["forum_name"] = str(request.get_json())
        print(session.get("forum_name"))
        return render_template('profile/search_patient.html')

@forum.route('/edit_profile', methods = ["GET", "POST"])
def edit():
    form = editBio()
    if form.validate_on_submit():
        try:
            bioEditor(form)
            return redirect(url_for('forum.home'))
        except:
            flash("Error Creating Forum")
            return redirect(url_for('forum.home'))
    forum_pro = Forum_profile.query.filter(Forum_profile.user_id == current_user.user_id).first()
    return render_template('forum/edit_bio.html', form = form, forum_pro = forum_pro)

def bioEditor(form):
    #edit the bio
    forum_pro = Forum_profile.query.filter(Forum_profile.user_id == current_user.user_id).first()
    forum_pro.username = form.username.data
    forum_pro.bio = form.bio.data
    db.session.commit()
