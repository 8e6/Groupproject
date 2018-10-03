from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, BooleanField, TextAreaField, SelectField, SelectMultipleField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from ..models import Programme, Company


class AcademicYearForm(FlaskForm):
    year = StringField('Year', validators=[DataRequired()])
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DomainForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class FaqForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    rank = IntegerField('Rank')
    external = BooleanField('External', validators=[DataRequired()], default=False)
    student = BooleanField('Student', validators=[DataRequired()], default=False)
    submit = SubmitField('Submit')


class FlagForm(FlaskForm):
    project_id = SelectField('Project', coerce=int)
    user_id = SelectField('User', coerce=int)
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ProgrammeForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ProjectForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    client_id = SelectField('Client', coerce=int)
    overview = TextAreaField('Overview', validators=[DataRequired()])
    deliverables = TextAreaField('Deliverables', validators=[DataRequired()])
    resources = TextAreaField('Resources', validators=[DataRequired()])
    skills_required = SelectMultipleField('Skills required', coerce=int)
    academic_year = SelectField('Academic year')
    status_id = SelectField('Status', coerce=int)
    submit = SubmitField('Submit')


class CompanyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    post_code = StringField('Post code', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SettingsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    last_notification_check = DateField('Last notification check', validators=[DataRequired()])
    submit = SubmitField('Submit')


class SkillForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class StatusForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    domain_id = SelectField('Domain', coerce=int)
    action_text = StringField('Action text')
    css_class = StringField('css class')
    default_for_domain = BooleanField('Default for domain')
    submit = SubmitField('Submit')


class TeamForm(FlaskForm):
    project_id = SelectField('Project', coerce=int)
    created_by = SelectField('Created by', coerce=int)
    members = SelectMultipleField('Members', coerce=int)
    comment = StringField('Profile comment')
    vacancies = StringField('Vacancies message')
    status_id = SelectField('Status', coerce=int)
    submit = SubmitField('Submit')


class TransitionForm(FlaskForm):
    from_status_id = SelectField('From status', coerce=int)
    to_status_id = SelectField('To status', coerce=int)
    submit = SubmitField('Submit')


class UserAssignForm(FlaskForm):
    programme = QuerySelectField(query_factory=lambda: Programme.query.all(), get_label="code")
    company = QuerySelectField(query_factory=lambda: Company.query.all(), get_label="name")
    submit = SubmitField('Submit')
