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
        return HTMLString('<button %s> Confirm Checkup' % self.html_params(name=field.name, **kwargs))



class InlineSubmitField(BooleanField):
    """
    Represents an ``<button type="submit">``.  This allows checking if a given
    submit button has been pressed.
    """
    widget = InlineButtonWidget()


class NewHealthCheckForm(FlaskForm):
    height = IntegerField("Enter Height in Centimeters", validators = [Required()])
    weight = IntegerField("Enter Weight", validators = [Required()])
    blood_pressure = IntegerField("Enter Blood Pressure", validators = [Required()])
    bt = [(0, "O-"), (1, "O+"),(2, "A-"),(3, "A+"),(4, "B-"),(5, "B+"),(6, "AB-"),(7, "AB+")]
    blood_type = SelectField("blood_type", coerce=int, default = 0,  choices = bt)
    gender = SelectField("gender", coerce=int, default = 0, choices=[(0, "Female"),(1, "Male")])
    description = TextAreaField('Enter a description', validators = [Required(), Length(max=2000)])
    submit = InlineSubmitField('Confim Checkup Information')

    #When a form defines a method with the prefix validate_ followed by the name of a fiel0d,
    # #the method is invoked in addition to any regularly defined validators
    def validate_form(self, form):
        form.blood_type = int(form.blood_type.data)
        form.gender = int(form.gender.data)
        print("checking sheet")
        if height.data <= 0:
            raise ValidationError('Enter a height greater than 0')
        if weight.data <= 0:
            raise ValidationError('Enter a weight greater than 0')
