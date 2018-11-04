from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Optional


class ProfileForm(FlaskForm):
    email = StringField('Email', render_kw={'disabled':''}, validators=[DataRequired()])
    username = StringField('Username', render_kw={'disabled':''}, validators=[DataRequired()])
    first_name = StringField('First name', render_kw={'disabled':''}, validators=[DataRequired()])
    last_name = StringField('Last name', render_kw={'disabled':''}, validators=[DataRequired()])
    profile_comment = TextAreaField('Profile comment')
    skills_offered = SelectMultipleField('Skills offered', coerce=int)
    submit = SubmitField('Submit')


class FlagForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Save')

class TeamForm(FlaskForm):
    comment = TextAreaField('Team profile comment', validators=[DataRequired()])
    vacancies = TextAreaField('Vacancies message')
    matric = StringField('Add team member')
    submit = SubmitField('Save')


