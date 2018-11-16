from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_required
from collections import Counter

from sqlalchemy import and_, or_

from . import staff
from .forms import *


@staff.route('/staff_dashboard')
@login_required
def dashboard():
    skill = request.args.get("skill")
    company = request.args.get("company")
    project_domain = Domain.query.filter(Domain.name == 'project').first()
    statuses = Status.query.filter(and_(Status.domain_id == project_domain.id,
                                        or_(Status.name == 'Live',
                                            Status.name == 'Withdrawn',
                                            Status.name == 'Complete'))).with_entities(Status.id)
    projects = Project.query.filter(Project.status_id.in_(statuses))
    skills = []
    for project in projects:
        skills += [(s.skill_required.id, s.skill_required.name) for s in project.skills_required]
    skills = Counter(skills)
    companies = []
    companies += [(p.client.company.id, p.client.company.name) for p in projects]
    companies = Counter(companies)
    return render_template('staff/dashboard.html',
                           projects=projects,
                           skills=skills,
                           skill=skill,
                           companies=companies,
                           company=company,
                           title="Dashboard")


@staff.route('/staff/profile/edit', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(current_user.id)
    form = ProfileForm(obj=user)

    if form.validate_on_submit():
        user.profile_comment = form.profile_comment.data
        db.session.commit()
        flash('Profile updated')
        return redirect(url_for('staff.dashboard'))

    if form.errors:
        for field in form.errors:
            for error in form.errors[field]:
                flash(error, 'error')

    return render_template('staff/profile/profile.html', user=user, form=form, title="Edit profile")


@staff.route('/project/<int:id>')
@login_required
def project(id):
    project = Project.query.get(id)
    interest = Interest.query.filter(and_(Interest.project_id == id, Interest.user_id == current_user.id)).first()
    flag = Flag.query.filter(and_(Flag.project_id == id, Flag.user_id == current_user.id)).first()
    teams = Team.query.filter(Team.project_id == id)
    team_member = TeamMember.query.filter(and_(TeamMember.user_id == current_user.id,
                                               TeamMember.team_id.in_([t.id for t in teams]))).first()
    return render_template('staff/projects/project.html',
                           project=project,
                           interest=interest,
                           flag=flag,
                           team_member=team_member,
                           title='View project')


@staff.route('/vacancies', methods=['GET', 'POST'])
@login_required
def vacancies():
    teams = Team.query.filter(Team.vacancies != None).all()
    return render_template('staff/projects/vacancies.html', teams=teams, title="Vacancies")


