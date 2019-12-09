from flask import Blueprint

files_uploaded = Blueprint('files_uploaded',__name__, url_prefix='/templates')

from . import views
