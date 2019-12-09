from flask import Blueprint

pdf_viewer = Blueprint('pdf_viewer',__name__)

from . import views
