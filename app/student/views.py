from flask import abort, render_template, flash, redirect, url_for, current_app, request
from flask_login import current_user, login_required
from flask_mail import Message, Mail
from collections import Counter
import logging

from sqlalchemy import and_, or_, text, delete
from sqlalchemy.orm.exc import NoResultFound

from app.models import *
from . import student
from .forms import *


@student.route('/student_dashboard')
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
    return render_template('student/dashboard.html',
                           projects=projects,
                           skills=skills,
                           skill=skill,
                           companies=companies,
                           company=company,
                           title="Dashboard")


@student.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(current_user.id)
    form = ProfileForm(obj=user)
    form.skills_offered.choices = [(s.id, s.name) for s in Skill.query.order_by(text('name'))]
    form.skills_offered.data = [s.skill_id for s in user.skills_offered]

    if form.validate_on_submit():
        user.profile_comment = form.profile_comment.data
        SkillOffered.query.filter(SkillOffered.user_id==current_user.id).delete()
        for skill in form.skills_offered.raw_data:
            skill_offered = SkillOffered(user_id=current_user.id, skill_id=skill)
            db.session.add(skill_offered)
        db.session.commit()
        flash('Profile updated')
        return redirect(url_for('student.dashboard'))

    if form.errors:
        for field in form.errors:
            for error in form.errors[field]:
                flash(error, 'error')

    return render_template('student/profile/profile.html', user=user, form=form, title="Edit profile")


@student.route('/projects')
@login_required
def projects():
    project_domain = Domain.query.filter(Domain.name == 'project').first()
    statuses = Status.query.filter(and_(Status.id == project_domain.id,
                                        or_(Status.name == 'Live',
                                            Status.name == 'Withdrawn',
                                            Status.name == 'Complete')))
    projects = Project.query.filter(Project.status in statuses).all()
    return render_template('student/projects/projects.html', projects=projects, title="Projects")


@student.route('/project/<int:id>')
@login_required
def project(id):
    project = Project.query.get(id)
    interest = Interest.query.filter(and_(Interest.project_id == id, Interest.user_id == current_user.id)).first()
    flag = Flag.query.filter(and_(Flag.project_id == id, Flag.user_id == current_user.id)).first()
    teams = Team.query.filter(Team.project_id == id)
    team_member = TeamMember.query.filter(and_(TeamMember.user_id == current_user.id,
                                               TeamMember.team_id.in_([t.id for t in teams]))).first()
    return render_template('student/projects/project.html',
                           project=project,
                           interest=interest,
                           flag=flag,
                           team_member=team_member,
                           title='View project')


@student.route('/interest/add/<int:id>', methods=['GET', 'POST'])
@login_required
def add_interest(id):
    interest = Interest(
        project_id=id,
        user_id=current_user.id
    )
    db.session.add(interest)
    db.session.commit()
    flash('Interest noted')

    return redirect(url_for('.project', id=id))


@student.route('/interest/delete/<int:project_id>/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_interest(project_id, id):
    interest = Interest.query.get(id)
    db.session.delete(interest)
    db.session.commit()
    flash('Interest deleted')

    return redirect(url_for('.project', id=project_id))


@student.route('/team/create/<int:project_id>', methods=['GET', 'POST'])
@login_required
def create_team(project_id):
    add_team = True

    domain = Domain.query.filter(Domain.name == 'team').first()
    new_status = Status.query.filter(and_(Status.domain_id==domain.id, Status.name=='New')).first()

    form = TeamForm()
    settings = Settings.query.first()

    if form.validate_on_submit():
        team = Team(project_id = project_id,
                    created_by = current_user.id,
                    comment = form.comment.data,
                    vacancies = form.vacancies.data,
                    status_id = new_status.id)

        try:
            db.session.add(team)
            db.session.commit()
            db.session.refresh(team)
            team_member = TeamMember(user_id=current_user.id, team_id=team.id)
            db.session.add(team_member)
            db.session.commit()
            flash('Team created')
        except:
            flash('There was a problem creating the team', 'error')

        return redirect(url_for('student.edit_team', project_id=project_id, id=team.id))

    return render_template('student/teams/team.html',
                           settings=settings,
                           add_team=add_team,
                           form=form,
                           title='Create team')


@student.route('/team/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team(id):
    add_team = False
    settings = Settings.query.first()

    team = Team.query.get(id)
    form = TeamForm(obj=team)
    # form.comment.data = team.comment
    # form.vacancies.data = team.vacancies

    if form.validate_on_submit():
        team.comment=form.comment.data
        team.vacancies=form.vacancies.data
        db.session.add(team)

        if form.matric.data is not None:
            try:
                member = User.query.filter(User.username==form.matric.data)
                team_member = TeamMember(user_id=member.id, team_id=team.id)
                db.session.add(team_member)
            except NoResultFound:
                flash('Matric number not recognised', 'error')
            except AttributeError:
                pass

        try:
            db.session.commit()
            flash('Team updated')
        except:
            flash('There was a problem updating the team', 'error')

        return redirect(url_for('student.edit_team', id=team.id))

    return render_template('student/teams/team.html',
                           settings=settings,
                           add_team=add_team,
                           team=team,
                           form=form,
                           title='Edit team')


@student.route('/member/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_member(id):
    team_member = TeamMember.query.get(id)
    team = team_member.team
    if len(team.members) == 1:
        return redirect(url_for('student.delete_team', id=team.id))

    db.session.delete(team_member)
    db.session.commit()
    flash('Team member deleted')

    return redirect(url_for('.edit_team', id=team.id))


@student.route('/team/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_team(id):
    team = Team.query.get(id)
    project_id = team.project_id
    db.session.delete(team)
    db.session.commit()
    flash('Team deleted')

    return redirect(url_for('.project', id=project_id))


@student.route('/flag/set/<int:id>', methods=['GET', 'POST'])
@login_required
def set_flag(id):
    form = FlagForm()
    add_flag = True

    if form.validate_on_submit():
        flag = Flag(user_id = current_user.id,
                    project_id = id,
                    message = form.message.data)
        try:
            db.session.add(flag)
            db.session.commit()
            flash('Flag set')
            return redirect(url_for('student.project', id=id))
        except Exception as e:
            flash('Error: ' + str(e))

    if form.errors:
        for field in form.errors:
            for error in form.errors[field]:
                flash(error, 'error')

    return render_template('student/flags/flag.html', form=form, add_flag=add_flag, title="Flag project")


@student.route('/flag/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_flag(id):
    flag = Flag.query.get(id)
    form = FlagForm(obj=flag)
    add_flag = False

    if form.validate_on_submit():
        flag.message = form.message.data
        try:
            db.session.add(flag)
            db.session.commit()
            flash('Flag updated')
            return redirect(url_for('student.project', id=flag.project_id))
        except Exception as e:
            flash('Error: ' + str(e))

    if form.errors:
        for field in form.errors:
            for error in form.errors[field]:
                flash(error, 'error')

    return render_template('student/flags/flag.html', form=form, add_flag=add_flag, flag=flag, title="Edit flag")


@student.route('/flag/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_flag(id):
    flag = Flag.query.get(id)
    project_id = flag.project_id
    db.session.delete(flag)
    db.session.commit()
    flash('Flag deleted')

    return redirect(url_for('.project', id=project_id))


@student.route('/vacancies', methods=['GET', 'POST'])
@login_required
def vacancies():
    teams = Team.query.filter(Team.vacancies != None).all()
    return render_template('student/projects/vacancies.html', teams=teams, title="Vacancies")


