from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, BooleanField, TextAreaField, SelectField, SelectMultipleField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from ..models import Programme, Company

class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    overview = TextAreaField('Overview', validators=[DataRequired()])
    deliverables = TextAreaField('Deliverables', validators=[DataRequired()])
    resources = TextAreaField('Resources', validators=[DataRequired()])
    skills_required = SelectMultipleField('Skills required', coerce=int)
    academic_year = SelectField('Academic year')
    submit = SubmitField('Submit')
