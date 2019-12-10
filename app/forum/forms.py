from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, IntegerField, TextField, TextAreaField#,DateField
from wtforms.validators import Required, Email, Length, Regexp, EqualTo, NumberRange
from wtforms import ValidationError
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
from datetime import datetime, date
from .. import db
from ..models import User, Hospital, Forum
from wtforms.widgets.core import html_params
from wtforms.widgets import HTMLString

class PostForm(FlaskForm):
    text = TextAreaField('Post', validators = [Required(), Length(10,250)])
    submit = SubmitField('Post')

class createForumForm(FlaskForm):
    title = TextField('Forum Name', validators = [Required(), Length(5, 25)]) # Regexp(r'^[\w.@+-]+$'
    text = TextAreaField('Post', validators = [Required(), Length(10,250)])
    visibility = SelectField('Visibility', choices = [(0, "Please Select Visibility"),(1, "Public"), (2, "Private")], validators = [Required()], coerce = int)
    submit = SubmitField('Post')

    def validate_title(self, field):
        if Forum.query.filter(Forum.forum_name == field.data).first():
            raise ValidationError('Forum name already registered.')

    def validate_visibility(self, field):
        if field.data == 2:
            raise ValidationError('Please Select Visibility!')
