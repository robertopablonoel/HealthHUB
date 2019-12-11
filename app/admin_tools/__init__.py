from flask import Blueprint

admin_tools = Blueprint('admin_tools',__name__)

from . import views
