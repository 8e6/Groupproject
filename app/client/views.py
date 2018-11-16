from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql import text

from . import client
from .forms import *
from app.models import *


#--------  Profile views ----------#

@client.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(current_user.id)
    company_id = user.company_id
    new_company = user.company.is_new
    if new_company:
        form = ProfileFormWithCompany(obj=user)
        form.company_id.choices = [(user.company_id, user.company.name)] +\
                                  [(c.id, c.name) for c in Company.query.order_by(text('name')) if c.name != user.company.name]

        form.company_id.data = user.company_id
    else:
        form = ProfileForm(obj=user)

    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.telephone = form.telephone.data
        user.display_name_flag = form.display_name_flag.data
        user.display_email_flag = form.display_email_flag.data
        user.display_phone_flag = form.display_phone_flag.data
        user.company_id = form.company_id.raw_data[0]
        user.profile_comment = form.profile_comment.data
        db.session.commit()

        if user.company_id != company_id and new_company:
            db.session.expire_all()
            company = Company.query.get(company_id)
            db.session.delete(company)
            db.session.commit()
        flash('Profile updated')
        return redirect(url_for('home.dashboard'))

    if form.errors:
        for field in form.errors:
            for error in form.errors[field]:
                flash(error, 'error')

    form.email.data = user.email
    form.username.data = user.username
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.telephone.data = user.telephone
    form.display_name_flag = user.display_name_flag
    form.display_email_flag = user.display_email_flag
    form.display_phone_flag = user.display_phone_flag
    if user.company.is_new:
        form.company_id.data = user.company_id
    form.profile_comment.data = user.profile_comment
    return render_template('client/profile/profile.html', user=user, form=form, title="Update profile")


@client.route('/company', methods=['GET', 'POST'])
@login_required
def company():
    company = Company.query.filter(Company.id == current_user.company_id).first()
    form = CompanyForm(obj=company)

    if form.validate_on_submit():
        company.name = form.name.data
        company.description = form.description.data
        company.address = form.address.data
        company.city = form.city.data
        company.post_code = form.post_code.data
        company.web = form.web.data
        company.health_policy_flag = form.health_policy_flag.data
        company.health_policy_link = form.health_policy_link.data
        company.training_policy_flag = form.training_policy_flag.data
        company.training_policy_link = form.training_policy_link.data
        company.hse_registered = form.hse_registered.data
        company.la_registered = form.la_registered.data
        company.insured = form.insured.data
        company.student_insured = form.student_insured.data
        company.company_risk_assessed = form.company_risk_assessed.data
        company.risks_reviewed = form.risks_reviewed.data
        company.risks_mitigated = form.risks_mitigated.data
        company.accident_procedure_flag = form.accident_procedure_flag.data
        company.emergency_procedures_flag = form.emergency_procedures_flag.data
        company.report_student_accidents_flag = form.report_student_accidents_flag.data
        company.report_student_illness_flag = form.report_student_illness_flag.data
        company.data_policy_flag = form.data_policy_flag.data
        company.data_policy_link = form.data_policy_link.data
        company.security_measures_flag = form.security_measures_flag.data
        company.ico_registration_number = form.ico_registration_number.data
        company.data_training_flag = form.data_training_flag.data
        company.security_policy_flag = form.security_policy_flag.data
        company.security_policy_link = form.security_policy_link.data
        company.privacy_notice_flag = form.privacy_notice_flag.data
        company.data_contact_first_name = form.data_contact_first_name.data
        company.data_contact_last_name = form.data_contact_last_name.data
        company.data_contact_position = form.data_contact_position.data
        company.data_contact_telephone = form.data_contact_telephone.data

        db.session.add(company)
        db.session.commit()
        flash('Company details updated')

        return redirect(url_for('home.dashboard'))

    errors = form.errors
    if len(errors) > 0:
        for key, value in errors.items():
            flash(value[0], 'error')

    # if company.name != ' New company':
    #     form.name.data = company.name
    #     form.description.data = company.description
    #     form.address.data = company.address
    #     form.city.data = company.city
    #     form.post_code.data = company.post_code
    #     form.web.data = company.web
    #     form.health_policy_flag.data = company.health_policy_flag
    #     form.health_policy_link.data = company.health_policy_link
    #     form.training_policy_flag.data = company.training_policy_flag
    #     form.training_policy_link.data = company.training_policy_link
    #     form.hse_registered.data = company.hse_registered
    #     form.la_registered.data = company.la_registered
    #     form.insured.data = company.insured
    #     form.student_insured.data = company.student_insured
    #     form.company_risk_assessed.data = company.company_risk_assessed
    #     form.risks_reviewed.data = company.risks_reviewed
    #     form.risks_mitigated.data = company.risks_mitigated
    #     form.accident_procedure_flag.data = company.accident_procedure_flag
    #     form.emergency_procedures_flag.data = company.emergency_procedures_flag
    #     form.report_student_accidents_flag.data = company.report_student_accidents_flag
    #     form.report_student_illness_flag.data = company.report_student_illness_flag
    #     form.data_policy_flag.data = company.data_policy_flag
    #     form.data_policy_link.data = company.data_policy_link
    #     form.security_measures_flag.data = company.security_measures_flag
    #     form.ico_registration_number.data = company.ico_registration_number
    #     form.data_training_flag.data = company.data_training_flag
    #     form.security_policy_flag.data = company.security_policy_flag
    #     form.security_policy_link.data = company.security_policy_link
    #     form.privacy_notice_flag.data = company.privacy_notice_flag
    #     form.data_contact_first_name.data = company.data_contact_first_name
    #     form.data_contact_last_name.data = company.data_contact_last_name
    #     form.data_contact_position.data = company.data_contact_position
    #     form.data_contact_telephone.data = company.data_contact_telephone

    return render_template('client/profile/company.html',
                           company=company, form=form, title="Update company details")



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

        try:
            db.session.add(project)
            db.session.commit()
            db.session.refresh(project)
            for skill in skills_required:
                skill_required = SkillRequired(project_id=project.id, skill_id=skill)
                db.session.add(skill_required)
            db.session.commit()
            flash('You have successfully added a new project.')
        except:
            flash('Error: project id already exists.')

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
        project.updated_date = datetime.now()
        db.session.add(project)
        SkillRequired.query.filter(SkillRequired.project_id==project.id).delete()
        for skill in form.skills_required.raw_data:
            if skill not in [s.skill_id for s in project.skills_required]:
                skill_required = SkillRequired(project_id=project.id, skill_id=skill)
                db.session.add(skill_required)
        db.session.commit()
        flash('You have successfully edited the project.')

        return redirect(url_for('home.dashboard'))

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

@client.route('/projects/transition/<int:id>/<int:status_id>', methods=['GET', 'POST'])
@login_required
def transition(id, status_id):

    project = Project.query.get_or_404(id)
    status = Status.query.get(status_id)
    project.status_id = status.id
    db.session.add(project)
    db.session.commit()
    flash('The project status is now ' + status.name)

    return redirect(url_for('home.dashboard'))


