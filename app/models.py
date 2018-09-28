import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


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
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    address = db.Column(db.String(120), index=True)
    city = db.Column(db.String(60), index=True)
    post_code = db.Column(db.String(10))
    employees = db.relationship('User', backref='company', lazy='dynamic')

    def __repr__(self):
        return '<Company: {}>'.format(self.name)


class Programme(db.Model):
    __tablename__ = 'programme'

    code = db.Column(db.String(10), unique=True, primary_key=True)
    title = db.Column(db.String(200))

    def __repr__(self):
        return '<Programme: {}>'.format(self.title)



