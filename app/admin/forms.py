from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, IntegerField, BooleanField, TextAreaField, SelectField, SelectMultipleField, RadioField, Label
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
    external = BooleanField('External', default=False)
    student = BooleanField('Student', default=False)
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
    web = StringField('Web address')
    health_policy_flag = RadioField('Do you have a written Health and Safety policy?', choices=[(1,'yes'),(0,'no')], coerce=int)
    health_policy_link = StringField('Link to H&S policy')
    training_policy_flag = RadioField('Do you have a H&S training policy?', choices=[(1,'yes'),(0,'no')], coerce=int)
    training_policy_link = StringField('Link to H&S training policy')
    hse_registered = RadioField('Are you registered with the Health and Safety Executive?', choices=[(1,'yes'),(0,'no')], coerce=int)
    la_registered = RadioField('Are you registered with the local authority environmental health dept?', choices=[(1,'yes'),(0,'no')], coerce=int)
    insured = RadioField('Do you have public liability insurance?', choices=[(1,'yes'),(0,'no')], coerce=int)
    student_insured = RadioField('Does the PL policy cover the student(s)?', choices=[(1,'yes'),(0,'no')], coerce=int)
    company_risk_assessed = RadioField('Have you carried out a workplace risk assessment?', choices=[(1,'yes'),(0,'no')], coerce=int)
    risks_reviewed = RadioField('Are risks reviewed regularly?', choices=[(1,'yes'),(0,'no')], coerce=int)
    risks_mitigated = RadioField('Are risk assessment results implemented?', choices=[(1,'yes'),(0,'no')], coerce=int)
    accident_procedure_flag = RadioField('Do you have a procedure for reporting accidents?', choices=[(1,'yes'),(0,'no')], coerce=int)
    emergency_procedure_flag = RadioField('Do you have procedures for dealing with emergencies?', choices=[(1,'yes'),(0,'no')], coerce=int)
    report_student_accidents_flag = RadioField('Will all accidents involving the student be reported to the University?', choices=[(1,'yes'),(0,'no')], coerce=int)
    report_student_illness_flag = RadioField('Will any student illness attributable to the work be reported to the University?', choices=[(1,'yes'),(0,'no')], coerce=int)
    data_policy_flag = RadioField('Do you have a data protection policy?', choices=[(1,'yes'),(0,'no')], coerce=int)
    data_policy_link = StringField('Link to DP policy')
    security_measures_flag = RadioField('Do you have data protection/privacy measures in place?', choices=[(1,'yes'),(0,'no')], coerce=int)
    ico_registration_number = StringField('What is your registration number with the Information Commissioner\'s Office?')
    data_training_flag = RadioField('Do staff receive regular data protection training?', choices=[(1,'yes'),(0,'no')], coerce=int)
    security_policy_flag = RadioField('Do you have information security policies in place?', choices=[(1,'yes'),(0,'no')], coerce=int)
    security_policy_link = StringField('Link to information security policy')
    privacy_notice_flag = RadioField('Is there a staff privacy notice that would cover the student?', choices=[(1,'yes'),(0,'no')], coerce=int)
    data_contact_first_name = StringField('First name')
    data_contact_last_name = StringField('Last name')
    data_contact_position = StringField('Position')
    data_contact_telephone = StringField('Telephone')
    submit = SubmitField('Submit')


class SettingsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    subtitle = StringField('Subtitle', validators=[DataRequired()])
    notification_period = IntegerField('Notification period', validators=[DataRequired()])
    last_notification_check = DateField('Last notification check', validators=[DataRequired()])
    contact_name = StringField('Contact name', validators=[DataRequired()])
    contact_email = StringField('Contact email', validators=[DataRequired()])
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
    admin_only = BooleanField('Admin only')
    submit = SubmitField('Submit')


class UserAssignForm(FlaskForm):
    programme = QuerySelectField(query_factory=lambda: Programme.query.all(), get_label="code")
    company = QuerySelectField(query_factory=lambda: Company.query.all(), get_label="name")
    submit = SubmitField('Submit')

