from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask import json
from flask_apscheduler import APScheduler
# from .models import Forum
# import atexit
# from apscheduler.scheduler import Scheduler


bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
mail = Mail()
scheduler = APScheduler()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__, static_folder = 'templates')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    scheduler.init_app(app)
    scheduler.start()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix = '/auth')

    from .sched import sched as sched_blueprint
    app.register_blueprint(sched_blueprint, url_prefix = '/sched')

    from .roomres import roomres as roomres_blueprint
    app.register_blueprint(roomres_blueprint, url_prefix = '/roomres')

    from .forum import forum as forum_blueprint
    app.register_blueprint(forum_blueprint, url_prefix = '/forum')


    return app

def update_tables():
    top_forums = Forum.query.join(Forum_members, (Forum.forum_id == Forum_members.forum_id)) \
                            .with_entities(Forum.hospital_id, Forum.forum_id, Forum.db.func.count(Forum_members.user_id)) \
                            .group_by(Forum.hospital_id, Forum.forum_id).order_by(Forum.db.func.count(Forum_members.user_id).desc()).all()[:5]
    print(top_forums)
    top = Top_forums(top_forums)
