from flask import abort, render_template, flash, redirect, url_for, current_app
from flask_login import current_user, login_required
from flask_mail import Message, Mail
import logging

from app.models import *
from . import home
from .forms import *


@home.route('/')
def homepage():
    settings = Settings.query.first()
    return render_template('home/index.html', settings=settings, title="Welcome")


@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    unconfirmed_companies = User.query.filter(User.company_confirmed == 0).all()
    logged_in_users = User.query.filter(User.online_flag == True).all()
    projects = Project.query.order_by(Project.title).all()
    print(projects)
    project_domain = Status.query.filter(Domain.name == 'project').first()
    print(project_domain)
    status_new = Status.query.filter(Status.domain_id == project_domain.id).first()
    print(status_new)
    new_projects = Project.query.filter(Project.status_id == status_new.id).all()

    return render_template('home/admin_dashboard.html',
                           title="Dashboard",
                           unconfirmed_companies=unconfirmed_companies,
                           logged_in_users=logged_in_users,
                           projects=projects,
                           new_projects=new_projects
                           )


@home.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter(Project.client_id == current_user.id).all()
    from_statuses = [p.status_id for p in projects]
    transitions = Transition.query.filter(Transition.from_status_id.in_(from_statuses), Transition.admin_only == False).all()
    return render_template('home/dashboard.html', projects=projects, transitions=transitions, title="Dashboard")


@home.route('/faq', methods=['GET', 'POST'])
def faq():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        if user.is_admin:
            faqs = Faq.query.order_by(Faq.rank.desc()).all()
        elif user.is_external:
            faqs = Faq.query.filter(Faq.external == 1).order_by(Faq.rank.desc())
        else:
            faqs = Faq.query.filter(Faq.student == 1).order_by(Faq.rank.desc())
    else:
        faqs = Faq.query.filter(Faq.student == 0, Faq.external == 0).order_by(Faq.rank.desc())

    return render_template('home/faq.html', title="Frequently asked questions", faqs=faqs)


@home.route('/contact', methods=['GET', 'POST'])
def contact():
    settings = Settings.query.first()
    form = ContactForm()
    form.category.choices = [(1, 'Call back request'),
                             (2, 'Potential project'),
                             (3, 'Question'),
                             (4, 'Comment'),
                             (5, 'Bug report')
                            ]
    if form.validate_on_submit():
        try:
            msg = Message(subject="Project exchange " + [x[1] for x in form.category.choices if x[0] == form.category.data][0],
                          body=form.message.data,
                          sender=form.email.data,
                          recipients=[settings.contact_email])
            mail = Mail(current_app)
            mail.send(msg)
            flash('Thank you for your message')
        except:
            flash('There was a problem sending your message', 'error')

        if current_user.is_authenticated:
            user = User.query.get(current_user.id)
            if user.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            elif user.is_external:
                return redirect(url_for('home.dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            return redirect(url_for('home.homepage'))

    return render_template('home/contact.html', form=form, title='Contact')


@home.route('/privacy')
def privacy():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        if user.is_admin:
            return_path = 'home.admin_dashboard'
        elif user.is_external:
            return_path = 'home.dashboard'
        else:
            return_path = 'home.dashboard'
    else:
        return_path = 'home.index'

    return render_template('home/privacy.html', return_path=return_path, title='Privacy')
