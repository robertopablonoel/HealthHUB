from flask import Blueprint

health_check = Blueprint('health_check',__name__)

from . import views
