from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField,TextAreaField#,DateField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
from datetime import datetime, date
from .. import db
from ..models import User, Prescription
from wtforms.widgets.core import html_params
from wtforms.widgets import HTMLString



class InlineButtonWidget(object):
    """
    Render a basic ``<button>`` field.
    """
    input_type = 'submit'
    html_params = staticmethod(html_params)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('type', self.input_type)
        kwargs.setdefault('value', field.label.text)
        return HTMLString('<button %s> Confirm Prescription' % self.html_params(name=field.name, **kwargs))



class InlineSubmitField(BooleanField):
    """
    Represents an ``<button type="submit">``.  This allows checking if a given
    submit button has been pressed.
    """
    widget = InlineButtonWidget()


class NewPrescriptionForm(FlaskForm):
    expir_date = DateField('Expiration_Date', validators = [Required()])
    description = TextAreaField('Enter a description', validators = [Required(), Length(max=2000)])
    submit = InlineSubmitField('Confim Prescription')
    #When a form defines a method with the prefix validate_ followed by the name of a fiel0d,
    # #the method is invoked in addition to any regularly defined validators
    def validate_expir_date(self, field):
        if not field.data > date.today():
            raise ValidationError('Expiration Date Must be Later Than Today')
