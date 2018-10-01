import datetime
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class AcademicYear(db.Model):
    __tablename__ = 'academic_year'

    year = db.Column(db.String(7), primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date  = db.Column(db.DateTime, nullable=False)
    projects = db.relationship('Project', backref='year', lazy='select')

    def __repr__(self):
        return '<Academic year: {}>'.format(self.year)


class AlertQueue(db.Model):
    __tablename__ = 'alert_queue'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    email = db.Column(db.String(60), nullable=False)
    created_date = db.Column(db.DateTime, nullable=False, index=True)
    sent_date = db.Column(db.DateTime, index=True)
    subject = db.Column(db.String(120), nullable=False)
    message_text = db.Column(db.Text, nullable=False)


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    address = db.Column(db.String(120), index=True)
    city = db.Column(db.String(60), index=True)
    post_code = db.Column(db.String(10))
    employees = db.relationship('User', backref='company', lazy='joined')

    def __repr__(self):
        return '<Company: {}>'.format(self.name)


class Domain(db.Model):
    __tablename__ = 'domain'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    statuses = db.relationship('Status', backref='domain', lazy='select')

    def __repr__(self):
        return '<Domain: {}>'.format(self.name)


class Faq(db.Model):
    __tablename__ = 'faq'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(120), nullable=False)
    answer = db.Column(db.Text)
    rank = db.Column(db.Integer, default=0)
    external = db.Column(db.Boolean, default=False)
    student = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<FAQ: {}>'.format(self.question)


class Flag(db.Model):
    __tablename__ = 'flag'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    message = db.Column(db.Text)

    def __repr__(self):
        return '<Flag: {} {}, {}>'.format(self.user.first_name, self.user.last_name, self.project.title)


class Interest(db.Model):
    __tablename__ = 'interest'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Interest: {} {}, {}>'.format(self.user.first_name, self.user.last_name, self.project.title)


class Programme(db.Model):
    __tablename__ = 'programme'

    code = db.Column(db.String(10), unique=True, primary_key=True)
    title = db.Column(db.String(200))
    students = db.relationship('User', backref='programme', lazy='select')

    def __repr__(self):
        return '<Programme: {}>'.format(self.title)


class Project(db.Model):
    __tablename__ = 'project'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_date = db.Column(db.DateTime, default=datetime.datetime.now)
    academic_year = db.Column(db.String(7), db.ForeignKey('academic_year.year'), nullable=False, index=True)
    overview = db.Column(db.Text)
    deliverables = db.Column(db.Text)
    resources = db.Column(db.Text)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False, index=True)
    flags = db.relationship('Flag', backref='project', lazy='joined')
    notes_of_interest = db.relationship('Interest', backref='project', lazy='joined')
    skills_required = db.relationship('SkillRequired', backref='project', lazy='joined', cascade="all, delete", passive_deletes=True)
    teams = db.relationship('Team', backref='project', lazy='select')

    @property
    def status(self):
        return

    def __repr__(self):
        return '<Project: {}>'.format(self.title)


class Settings(db.Model):
    __tablename__ = 'settings'

    name = db.Column(db.String(60), primary_key=True)
    last_notification_check = db.Column(db.DateTime, nullable=False)


class Skill(db.Model):
    __tablename__ = 'skill'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    offered = db.relationship('SkillOffered', backref='skill_offered', lazy='select')
    required = db.relationship('SkillRequired', backref='skill_required', lazy='select')

    def __repr__(self):
        return '<Skill: {}>'.format(self.name)


class SkillOffered(db.Model):
    __tablename__ = 'skill_offered'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False, index=True)

    def __repr__(self):
        return '<Skill offered: {} {}, {}>'.format(self.user.first_name, self.user.last_name, self.skill.name)


class SkillRequired(db.Model):
    __tablename__ = 'skill_required'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id', ondelete="cascade"), nullable=False, index=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False, index=True)

    def __repr__(self):
        return '<Skill required: {}, {}>'.format(self.project.title, self.skill_required.name)


class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    domain_id = db.Column(db.Integer, db.ForeignKey('domain.id'), nullable=False, index=True)
    action_text = db.Column(db.String(10), nullable=False)
    css_class = db.Column(db.String(10), nullable=False)
    default_for_domain = db.Column(db.Boolean, nullable=False)
    projects = db.relationship('Project', backref='status', lazy='joined')
    teams = db.relationship('Team', backref='status', lazy='joined')
    # transitions_from = db.relationship('Transition', backref='from_status', lazy='select')
    # transitions_to = db.relationship('Transition', backref='to_status', lazy='select')

    def __repr__(self):
        return '<Status: {}>'.format(self.name)


class Transition(db.Model):
    __tablename__ = 'transition'

    id = db.Column(db.Integer, primary_key=True)
    from_status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False, index=True)
    to_status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False, index=True)
    from_status = relationship("Status", foreign_keys=[from_status_id])
    to_status = relationship("Status", foreign_keys=[to_status_id])

    def __repr__(self):
        return '<Status transition: {} - {}>'.format(self.from_status.name, self.to_status.name)


class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    updated_date = db.Column(db.DateTime, default=datetime.datetime.now)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False, index=True)
    comment = db.Column(db.Text)
    vacancies = db.Column(db.Text)
    members = db.relationship('TeamMember', backref='team', lazy='joined', cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return '<Team: {:d} {}>'.format(self.id, self.project.title)


class TeamMember(db.Model):
    __tablename__ = 'team_member'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id', ondelete='cascade'), nullable=False, index=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Team member: {} {} in team {:d}>'.format(self.user.first_name, self.user.last_name, self.id)


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    telephone = db.Column(db.String(60), index=True, unique=True)
    web = db.Column(db.String(120), index=True, unique=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    programme_code = db.Column(db.String(10), db.ForeignKey('programme.code'))
    profile_comment = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    is_external = db.Column(db.Boolean, default=False)
    notify_new = db.Column(db.Boolean, default=False)
    notify_interest = db.Column(db.Boolean, default=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.now)
    alerts = db.relationship('AlertQueue', backref='user', lazy='select')
    notes_of_interest = db.relationship('Interest', backref='user', lazy='select')
    projects_offered = db.relationship('Project', backref='client', lazy='joined')
    skills_offered = db.relationship('SkillOffered', backref='user', lazy='joined')
    flags = db.relationship('Flag', backref='user', lazy='select')
    members = db.relationship('TeamMember', backref='user', lazy='select')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
