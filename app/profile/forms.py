from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField #,DateField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
from datetime import datetime, date
from .. import db
from ..models import Prescription




class ModifyPrescriptionForm(FlaskForm):
    notify = SelectField('Notify', choices=[(0, "NO"), (1, "YES")])
    active = SelectField('Active', choices=[(0, "NO"), (1, "YES")])
    submit = SubmitField('Update')
    #When a form defines a method with the prefix validate_ followed by the name of a fiel0d,
    #the method is invoked in addition to any regularly defined validators
