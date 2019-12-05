from flask import Blueprint

prescript = Blueprint('prescript',__name__)

from . import views
