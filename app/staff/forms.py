from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Optional


class ProfileForm(FlaskForm):
    email = StringField('Email', render_kw={'disabled':''}, validators=[DataRequired()])
    username = StringField('Username', render_kw={'disabled':''}, validators=[DataRequired()])
    first_name = StringField('First name', render_kw={'disabled':''}, validators=[DataRequired()])
    last_name = StringField('Last name', render_kw={'disabled':''}, validators=[DataRequired()])
    profile_comment = TextAreaField('Profile comment')
    submit = SubmitField('Save')




