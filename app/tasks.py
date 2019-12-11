from flask import current_app
from rq import get_current_job
import celery
from celery.task.base import periodic_task, task
from app import create_app, db
from app.models import Forum, Forum_members, Top_forums, Post, Likes, Top_posts, Reaction, Task, Prescription, User
from app.email import send_email
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import os

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.app_context().push()

def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        # task.user.add_notification('task_progress', {'task_id': job.get_id(),
        #                                              'progress': progress})
        if progress >= 100:
            task.complete = True
        db.session.commit()

def update_forum(id):
    print('updating_forums')
    try:
        top = Forum.query.join(Forum_members, (Forum.forum_id == Forum_members.forum_id)) \
                                .with_entities(Forum.hospital_id, Forum.forum_id, db.func.count(Forum_members.user_id)) \
                                .group_by(Forum.hospital_id, Forum.forum_id).order_by(db.func.count(Forum_members.user_id).desc()).limit(25).all()
        Top_forums.query.delete()
        for i in range(len(top)):
            update_table = Top_forums(hospital_id = top[i][0],
                                        forum_id = top[i][1],
                                        subscribers = top[i][2])
            db.session.add(update_table)
        db.session.commit()
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())

def update_posts(id):
    print('updating_posts')
    try:
        top_likes = Post.query.join(Likes, (Post.post_id == Likes.post_id)).join(Forum, (Post.forum_id == Forum.forum_id)) \
                                .with_entities(Post.post_id, Post.forum_id, Forum.forum_name, db.func.count(Likes.user_id)) \
                                .group_by(Post.post_id, Post.forum_id, Forum.forum_name).order_by(db.func.count(Likes.user_id).desc()).limit(25).all()
        top_comments = Post.query.join(Reaction, (Post.post_id == Reaction.post_id)).join(Forum, (Post.forum_id == Forum.forum_id)) \
                                .with_entities(Post.post_id, Post.forum_id, Forum.forum_name, db.func.count(Reaction.reaction_id)) \
                                .group_by(Post.post_id, Post.forum_id, Forum.forum_name).order_by(db.func.count(Reaction.reaction_id).desc()).limit(25).all()
        print(top_likes)
        print(top_comments)
        Top_posts.query.delete()
        top_likes = top_likes + [i for i in top_comments if i not in top_likes]
        for i in range(len(top_likes)):
            update_table = Top_posts(post_id = top_likes[i][0],
                                        forum_id = top_likes[i][1],
                                        forum_name = top_likes[i][2])
            db.session.add(update_table)
        db.session.commit()
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())

def send_reminders(id, prescription, user):
    print("sending")
    try:
        user = user
        prescription = prescription
        prescription.last_notified = datetime.now()
        send_email(user.email, 'Reminder to take your Prescription',
                   'email/prescription_reminder', user=user, prescription=prescription)
    except:
        print("Error Sending")

@celery.task(name = "demo_task_name")
def queue_reminders():
    print("queuing")
    print(datetime.now())
    if datetime.now().hour < 23: # datetime.now().hour > 7 and
        print("here")
        notify = Prescription.query.filter(Prescription.notify == True).all()
        for prescript in notify:
            print("here")
            if prescript.last_notified  < datetime.now() - relativedelta(hours = prescript.time):
                print("here")
                user = User.query.filter(User.user_id == prescript.patient_id).first()
                current_app.task_queue.enqueue('app.tasks.' + "send_reminders", None, prescript, user)
