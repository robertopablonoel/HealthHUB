import os
from app import celery, create_app
from app import tasks
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app = app.app_context().push()
