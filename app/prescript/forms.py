from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField#,DateField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
from datetime import datetime, date
from .. import db
from ..models import Prescription


class NewPrescriptionForm(FlaskForm):
    expir_date = DateField('Expiration_Date', validators = [Required(), DateRange(date.today())])
    description = StringField('Enter a description', validators = [None, Length(max=2000)])
    submit = SubmitField('Submit')
    #When a form defines a method with the prefix validate_ followed by the name of a fiel0d,
    #the method is invoked in addition to any regularly defined validators
    def validate_patient(self, field):
        if Prescription.query.filter_by(patient_id = field.data).first() == None:
            raise ValidationError('This Patient does not Exist')
