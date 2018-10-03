from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql import text

from . import client
from .forms import *
from .. import db
from ..models import *


#--------  Project views ----------#

@client.route('/projects')
@login_required
def list_projects():
    projects = Project.query.filter(Project.client_id == current_user.id).all()
    return render_template('client/projects/projects.html', projects=projects, title='Projects')


@client.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    add_project = True

    form = ProjectForm()
    form.skills_required.choices = [(s.id, s.name) for s in Skill.query.order_by(text('name'))]
    project_domain = Domain.query.filter(Domain.name == 'project').first()
    default_status = Status.query.filter(Status.domain_id == project_domain.id,
                                         Status.default_for_domain == True).first()
    form.academic_year.choices = [(y.year, y.year) for y in AcademicYear.query.order_by(text('start_date'))]
    if form.validate_on_submit():
        skills_required = form.skills_required.data
        project = Project(title = form.title.data,
                          client_id = current_user.id,
                          overview = form.overview.data,
                          deliverables = form.deliverables.data,
                          resources = form.resources.data,
                          academic_year = form.academic_year.data,
                          status_id = default_status.id)

        # try:
        db.session.add(project)
        db.session.commit()
        db.session.refresh(project)
        for skill in skills_required:
            skill_required = SkillRequired(project_id=project.id, skill_id=skill)
            db.session.add(skill_required)
        db.session.commit()
        flash('You have successfully added a new project.')
        # except:
        #     flash('Error: project id already exists.')

        return redirect(url_for('home.dashboard'))

    return render_template('client/projects/project.html', add_project=add_project,
                           form=form, title='Add project')


@client.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    add_project = False

    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    form.academic_year.choices = [(y.year, y.year) for y in AcademicYear.query.order_by(text('start_date'))]
    form.skills_required.choices = [(s.id, s.name) for s in Skill.query.order_by(text('name'))]
    form.skills_required.data = [s.skill_id for s in project.skills_required]
    if form.validate_on_submit():
        project.title = form.title.data
        project.overview = form.overview.data
        project.deliverables = form.deliverables.data
        project.resources = form.resources.data
        project.academic_year = form.academic_year.data
        project.updated_date = datetime.datetime.now()
        db.session.add(project)
        for skill in form.skills_required.raw_data:
            if skill not in [s.skill_id for s in project.skills_required]:
                skill_required = SkillRequired(project_id=project.id, skill_id=skill)
                db.session.add(skill_required)
        for skill in project.skills_required:
            if skill.skill_id not in form.skills_required.raw_data:
                skill_required = SkillRequired.query.get(skill.id)
                db.session.delete(skill_required)
        db.session.commit()
        flash('You have successfully edited the project.')

        return redirect(url_for('home.dashboard'))

    form.title.data = project.title
    form.overview.data = project.overview
    form.deliverables.data = project.deliverables
    form.resources.data = project.resources
    form.academic_year.data = project.academic_year
    return render_template('client/projects/project.html', add_project=add_project,
                           project=project, form=form, title="Edit project")


@client.route('/projects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):

    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('You have successfully deleted the project.')

    return redirect(url_for('home.dashboard'))


