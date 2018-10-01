from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy.sql import text

from . import admin
from .forms import *
from .. import db
from ..models import *

def check_admin():
    if not current_user.is_admin:
        abort(403)


# --------  Academic year views ----------#

@admin.route('/academic_year', methods=['GET', 'POST'])
@login_required
def list_academic_years():
    check_admin()
    academic_years = AcademicYear.query.all()
    return render_template('admin/academic_years/academic_years.html', academic_years=academic_years, title="Academic Years")


@admin.route('/academic_years/add', methods=['GET', 'POST'])
@login_required
def add_academic_year():
    check_admin()
    add_academic_year = True

    form = AcademicYearForm()
    if form.validate_on_submit():
        academic_year = AcademicYear(year=form.year.data, start_date=form.start_date.data, end_date=form.end_date.data)
        try:
            db.session.add(academic_year)
            db.session.commit()
            flash('You have successfully added a new academic year.')
        except:
            flash('Error: academic year already exists.')

        return redirect(url_for('admin.list_academic_years'))

    return render_template('admin/academic_years/academic_year.html', action="Add",
                           add_academic_year=add_academic_year, form=form,
                           title="Add Academic Year")


@admin.route('/academic_years/edit/<year>', methods=['GET', 'POST'])
@login_required
def edit_academic_year(year):
    check_admin()
    add_academic_year = False

    academic_year = AcademicYear.query.get_or_404(year)
    form = AcademicYearForm(obj=academic_year)
    if form.validate_on_submit():
        academic_year.Year = form.year.data
        academic_year.start_date = form.start_date.data
        academic_year.end_date = form.end_date.data
        db.session.commit()
        flash('You have successfully edited the academic year.')

        return redirect(url_for('admin.list_academic_years'))

    form.year.data = academic_year.year
    form.start_date.data = academic_year.start_date
    form.end_date.data = academic_year.end_date
    return render_template('admin/academic_years/academic_year.html', action="Edit",
                           add_academic_year=add_academic_year, form=form,
                           academic_year=academic_year, title="Edit Academic Year")


@admin.route('/academic_years/delete/<year>', methods=['GET', 'POST'])
@login_required
def delete_academic_year(year):
    check_admin()

    academic_year = AcademicYear.query.get_or_404(year)
    db.session.delete(academic_year)
    db.session.commit()
    flash('You have successfully deleted the academic year.')

    return redirect(url_for('admin.list_academic_years'))


#--------  Programme views ----------#

@admin.route('/programmes', methods=['GET', 'POST'])
@login_required
def list_programmes():
    check_admin()
    programmes = Programme.query.all()

    return render_template('admin/programmes/programmes.html', programmes=programmes, title="Programmes")


@admin.route('/programmes/add', methods=['GET', 'POST'])
@login_required
def add_programme():
    check_admin()
    add_programme = True

    form = ProgrammeForm()
    if form.validate_on_submit():
        programme = Programme(code=form.code.data, title=form.title.data)
        try:
            db.session.add(programme)
            db.session.commit()
            flash('You have successfully added a new programme.')
        except:
            flash('Error: programme code already exists.')

        return redirect(url_for('admin.list_programmes'))

    return render_template('admin/programmes/programme.html', action="Add",
                           add_programme=add_programme, form=form,
                           title="Add Programme")


@admin.route('/programmes/edit/<code>', methods=['GET', 'POST'])
@login_required
def edit_programme(code):
    check_admin()
    add_programme = False

    programme = Programme.query.get_or_404(code)
    form = ProgrammeForm(obj=programme)
    if form.validate_on_submit():
        programme.code = form.code.data
        programme.title = form.title.data
        db.session.commit()
        flash('You have successfully edited the programme.')

        return redirect(url_for('admin.list_programmes'))

    form.title.data = programme.title
    form.code.data = programme.code
    return render_template('admin/programmes/programme.html', action="Edit",
                           add_programme=add_programme, form=form,
                           programme=programme, title="Edit Programme")


@admin.route('/programmes/delete/<code>', methods=['GET', 'POST'])
@login_required
def delete_programme(code):
    check_admin()

    programme = Programme.query.get_or_404(code)
    db.session.delete(programme)
    db.session.commit()
    flash('You have successfully deleted the programme.')

    return redirect(url_for('admin.list_programmes'))


#--------  Company views ----------#

@admin.route('/companies')
@login_required
def list_companies():
    check_admin()
    companies = Company.query.all()
    return render_template('admin/companies/companies.html',
                           companies=companies, title='Companies')


@admin.route('/companies/add', methods=['GET', 'POST'])
@login_required
def add_company():
    check_admin()
    add_company = True

    form = CompanyForm()
    if form.validate_on_submit():
        company = Company(name=form.name.data,
                          description=form.description.data,
                          address=form.address.data,
                          city=form.city.data,
                          post_code=form.post_code.data
                          )

        try:
            db.session.add(company)
            db.session.commit()
            flash('You have successfully added a new company.')
        except:
            flash('Error: company id already exists.')

        return redirect(url_for('admin.list_companies'))

    return render_template('admin/companies/company.html', add_company=add_company,
                           form=form, title='Add Company')


@admin.route('/companies/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_company(id):
    check_admin()
    add_company = False

    company = Company.query.get_or_404(id)
    form = CompanyForm(obj=company)
    if form.validate_on_submit():
        company.id = form.id.data
        company.name = form.name.data
        company.description = form.description.data
        company.address = form.address.data
        company.city = form.city.data
        company.post_code = form.post_code.data
        db.session.add(company)
        db.session.commit()
        flash('You have successfully edited the company.')

        return redirect(url_for('admin.list_companies'))

    form.name.id = company.id
    form.name.data = company.name
    form.description.data = company.description
    form.address.data = company.address
    form.city.data = company.city
    form.post_code.data = company.post_code
    return render_template('admin/companies/company.html', add_company=add_company,
                           form=form, title="Edit Company")


@admin.route('/companies/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_company(id):
    check_admin()

    company = Company.query.get_or_404(id)
    db.session.delete(company)
    db.session.commit()
    flash('You have successfully deleted the company.')

    return redirect(url_for('admin.list_companies'))


#--------  Domain views ----------#

@admin.route('/domains')
@login_required
def list_domains():
    check_admin()
    domains = Domain.query.all()
    return render_template('admin/domains/domains.html',
                           domains=domains, title='Domains')


@admin.route('/domains/add', methods=['GET', 'POST'])
@login_required
def add_domain():
    check_admin()
    add_domain = True

    form = DomainForm()
    if form.validate_on_submit():
        domain = Domain(name=form.name.data, description=form.description.data)

        try:
            db.session.add(domain)
            db.session.commit()
            flash('You have successfully added a new domain.')
        except:
            flash('Error: domain id already exists.')

        return redirect(url_for('admin.list_domains'))

    return render_template('admin/domains/domain.html', add_domain=add_domain,
                           form=form, title='Add Domain')


@admin.route('/domains/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_domain(id):
    check_admin()
    add_domain = False

    domain = Domain.query.get_or_404(id)
    form = DomainForm(obj=domain)
    if form.validate_on_submit():
        domain.id = form.id.data
        domain.name = form.name.data
        domain.description = form.description.data
        db.session.add(domain)
        db.session.commit()
        flash('You have successfully edited the domain.')

        return redirect(url_for('admin.list_domains'))

    form.name.id = domain.id
    form.name.data = domain.name
    form.description.data = domain.description
    return render_template('admin/domains/domain.html', add_domain=add_domain,
                           form=form, title="Edit Domain")


@admin.route('/domains/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_domain(id):
    check_admin()

    domain = Domain.query.get_or_404(id)
    db.session.delete(domain)
    db.session.commit()
    flash('You have successfully deleted the domain.')

    return redirect(url_for('admin.list_domains'))


#--------  FAQ views ----------#

@admin.route('/faqs')
@login_required
def list_faqs():
    check_admin()
    faqs = Faq.query.all()
    return render_template('admin/faqs/faqs.html', faqs=faqs, title='FAQs')


@admin.route('/faqs/add', methods=['GET', 'POST'])
@login_required
def add_faq():
    check_admin()
    add_faq = True

    form = FaqForm()
    if form.validate_on_submit():
        faq = Faq(name=form.name.data, description=form.description.data)

        try:
            db.session.add(faq)
            db.session.commit()
            flash('You have successfully added a new FAQ.')
        except:
            flash('Error: FAQ id already exists.')

        return redirect(url_for('admin.list_faqs'))

    return render_template('admin/faqs/faq.html', add_faq=add_faq,
                           form=form, title='Add FAQ')


@admin.route('/faqs/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_faq(id):
    check_admin()
    add_faq = False

    faq = Faq.query.get_or_404(id)
    form = FaqForm(obj=faq)
    if form.validate_on_submit():
        faq.id = form.id.data
        faq.question = form.question.data
        faq.answer = form.answer.data
        faq.rank = form.rank.data
        faq.external = form.external.data
        faq.student = form.student.data
        db.session.add(faq)
        db.session.commit()
        flash('You have successfully edited the faq.')

        return redirect(url_for('admin.list_faqs'))

    form.name.id = faq.id
    form.name.data = faq.name
    form.description.data = faq.description
    return render_template('admin/faqs/faq.html', add_faq=add_faq,
                           form=form, title="Edit FAQ")


@admin.route('/faqs/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_faq(id):
    check_admin()

    faq = Faq.query.get_or_404(id)
    db.session.delete(faq)
    db.session.commit()
    flash('You have successfully deleted the FAQ.')

    return redirect(url_for('admin.list_faqs'))


#--------  Flag views ----------#

@admin.route('/flags')
@login_required
def list_flags():
    check_admin()
    flags = Flag.query.all()
    return render_template('admin/flags/flags.html', flags=flags, title='Flags')


@admin.route('/flags/add', methods=['GET', 'POST'])
@login_required
def add_flag():
    check_admin()
    add_flag = True

    form = FlagForm()
    form.user_id.choices = [(u.id, u.first_name + ' ' + u.last_name) for u in User.query.order_by(text('last_name'))]
    form.project_id.choices = [(p.id, p.title) for p in Project.query.order_by(text('title'))]
    if form.validate_on_submit():
        flag = Flag(user_id = form.user_id.data,
                    project_id=form.project_id.data,
                    message=form.message.data)
        try:
            db.session.add(flag)
            db.session.commit()
            flash('You have successfully added a new flag.')
        except:
            flash('Error: flag id already exists.')

        return redirect(url_for('admin.list_flags'))

    return render_template('admin/flags/flag.html', add_flag=add_flag,
                           form=form, title='Add flag')


@admin.route('/flags/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_flag(id):
    check_admin()
    add_flag = False

    flag = Flag.query.get_or_404(id)
    form = FlagForm(obj=flag)
    form.user_id.choices = [(u.id, u.first_name + ' ' + u.last_name) for u in User.query.order_by(text('last_name'))]
    form.project_id.choices = [(p.id, p.title) for p in Project.query.order_by(text('title'))]
    if form.validate_on_submit():
        flag.user_id = form.user_id.data
        flag.project_id = form.project_id.data
        flag.message = form.message.data
        db.session.add(flag)
        db.session.commit()
        flash('You have successfully edited the flag.')

        return redirect(url_for('admin.list_flags'))

    form.user_id.data = flag.user_id
    form.project_id.data = flag.project_id
    form.message.data = flag.message
    return render_template('admin/flags/flag.html', add_flag=add_flag,
                           form=form, title="Edit flag")


@admin.route('/flags/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_flag(id):
    check_admin()

    flag = Flag.query.get_or_404(id)
    db.session.delete(flag)
    db.session.commit()
    flash('You have successfully deleted the flag.')

    return redirect(url_for('admin.list_flags'))


#--------  Project views ----------#

@admin.route('/projects')
@login_required
def list_projects():
    check_admin()
    projects = Project.query.all()
    return render_template('admin/projects/projects.html', projects=projects, title='Projects')


@admin.route('/projects/add', methods=['GET', 'POST'])
@login_required
def add_project():
    check_admin()
    add_project = True

    form = ProjectForm()
    form.client_id.choices = [(c.id, c.first_name + ' ' + c.last_name) for c in User.query.order_by(text('last_name'))]
    form.skills_required.choices = [(s.id, s.name) for s in Skill.query.order_by(text('name'))]
    project_domain = Domain.query.filter(Domain.name == 'project').first()
    form.status_id.choices = [(s.id, s.name) for s in Status.query.filter(Status.domain_id == project_domain.id).order_by(text('status.name'))]
    default_status = Status.query.filter(Status.domain_id == project_domain.id,
                                         Status.default_for_domain == True).first()
    form.status_id.default = default_status.id
    form.academic_year.choices = [(y.year, y.year) for y in AcademicYear.query.order_by(text('start_date'))]
    form.status_id.data = default_status.id
    if form.validate_on_submit():
        skills_required = form.skills_required.data
        project = Project(title = form.title.data,
                          client_id = form.client_id.data,
                          overview = form.overview.data,
                          deliverables = form.deliverables.data,
                          resources = form.resources.data,
                          academic_year = form.academic_year.data,
                          status_id = form.status_id.data)

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

        return redirect(url_for('admin.list_projects'))

    return render_template('admin/projects/project.html', add_project=add_project,
                           form=form, title='Add project')


@admin.route('/projects/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    check_admin()
    add_project = False

    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    form.client_id.choices = [(c.id, c.first_name + ' ' + c.last_name) for c in User.query.order_by(text('last_name'), text('first_name'))]
    project_domain = Domain.query.filter(Domain.name == 'project').first()
    form.status_id.choices = [(s.id, s.name) for s in Status.query.filter(Status.domain_id == project_domain.id).order_by(text('status.name'))]
    form.academic_year.choices = [(y.year, y.year) for y in AcademicYear.query.order_by(text('start_date'))]
    form.skills_required.choices = [(s.id, s.name) for s in Skill.query.order_by(text('name'))]
    form.skills_required.data = [s.skill_id for s in project.skills_required]
    if form.validate_on_submit():
        project.title = form.title.data
        project.client_id = form.client_id.data
        project.overview = form.overview.data
        project.deliverables = form.deliverables.data
        project.resources = form.resources.data
        project.academic_year = form.academic_year.data
        project.status_id = form.status_id.data
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

        return redirect(url_for('admin.list_projects'))

    form.title.data = project.title
    form.client_id.data = project.client_id
    form.overview.data = project.overview
    form.deliverables.data = project.deliverables
    form.resources.data = project.resources
    form.academic_year.data = project.academic_year
    form.status_id.data = project.status_id
    return render_template('admin/projects/project.html', add_project=add_project,
                           project=project, form=form, title="Edit project")


@admin.route('/projects/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_project(id):
    check_admin()

    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('You have successfully deleted the project.')

    return redirect(url_for('admin.list_projects'))


#--------  Settings views ----------#

@admin.route('/settings', methods=['GET', 'POST'])
@login_required
def update_settings():
    check_admin()

    settings = Settings.query.first()
    form = SettingsForm(obj=settings)
    if form.validate_on_submit():
        settings.name=form.name.data,
        settings.last_notification_check=form.last_notification_check.data

        try:
            db.session.add(settings)
            db.session.commit()
            flash('You have successfully updated the settings.')
        except:
            flash('Error: settings not updated.')

        return redirect(url_for('home.admin_dashboard'))

    form.name.data = settings.name
    form.last_notification_check.data = settings.last_notification_check

    return render_template('admin/settings/settings.html', form=form, title='Settings')


#--------  Skill views ----------#

@admin.route('/skills')
@login_required
def list_skills():
    check_admin()
    skills = Skill.query.order_by(text('name')).all()
    return render_template('admin/skills/skills.html', skills=skills, title='skills')


@admin.route('/skills/add', methods=['GET', 'POST'])
@login_required
def add_skill():
    check_admin()
    add_skill = True

    form = SkillForm()
    if form.validate_on_submit():
        skill = Skill(name = form.name.data, description = form.domain_id.data)

        try:
            db.session.add(skill)
            db.session.commit()
            flash('You have successfully added a new skill.')
        except:
            flash('Error: skill id already exists.')

        return redirect(url_for('admin.list_skills'))

    return render_template('admin/skills/skill.html', add_skill=add_skill,
                           form=form, title='Add skill')


@admin.route('/skills/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_skill(id):
    check_admin()
    add_skill = False

    skill = Skill.query.get_or_404(id)
    form = SkillForm(obj=skill)
    if form.validate_on_submit():
        skill.name = form.name.data
        skill.description = form.description.data
        db.session.add(skill)
        db.session.commit()
        flash('You have successfully edited the skill.')

        return redirect(url_for('admin.list_skills'))

    form.name.data = skill.name
    form.description.data = skill.description

    return render_template('admin/skills/skill.html', add_skill=add_skill,
                           form=form, title="Edit skill")


@admin.route('/skills/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_skill(id):
    check_admin()

    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash('You have successfully deleted the skill.')

    return redirect(url_for('admin.list_skills'))


#--------  Status views ----------#

@admin.route('/statuses')
@login_required
def list_statuses():
    check_admin()
    statuses = Status.query.all()
    return render_template('admin/statuses/statuses.html', statuses=statuses, title='Statuses')


@admin.route('/statuses/add', methods=['GET', 'POST'])
@login_required
def add_status():
    check_admin()
    add_status = True

    form = StatusForm()
    form.domain_id.choices = [(d.id, d.name) for d in Domain.query.order_by(text('name'))]
    if form.validate_on_submit():
        status = Status(name = form.name.data,
                        domain_id = form.domain_id.data,
                        action_text = form.action_text.data,
                        css_class = form.css_class.data,
                        default_for_domain = form.default_for_domain.data
                        )

        try:
            db.session.add(status)
            db.session.commit()
            flash('You have successfully added a new status.')
        except:
            flash('Error: status id already exists.')

        return redirect(url_for('admin.list_statuses'))

    return render_template('admin/statuses/status.html', add_status=add_status,
                           form=form, title='Add status')


@admin.route('/statuses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_status(id):
    check_admin()
    add_status = False

    status = Status.query.get_or_404(id)
    form = StatusForm(obj=status)
    form.domain_id.choices = [(d.id, d.name) for d in Domain.query.order_by(text('name'))]
    if form.validate_on_submit():
        status.name = form.name.data
        status.domain_id = form.domain_id.data
        status.action_text = form.action_text.data
        status.css_class = form.css_class.data
        status.default_for_domain = form.default_for_domain.data
        db.session.add(status)
        db.session.commit()
        flash('You have successfully edited the status.')

        return redirect(url_for('admin.list_statuses'))

    form.name.data = status.name
    form.domain_id.data = status.domain_id
    form.action_text.data = status.action_text
    form.css_class.data = status.css_class
    form.default_for_domain.data = status.default_for_domain

    return render_template('admin/statuses/status.html', add_status=add_status,
                           form=form, title="Edit status")


@admin.route('/statuses/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_status(id):
    check_admin()

    status = Status.query.get_or_404(id)
    db.session.delete(status)
    db.session.commit()
    flash('You have successfully deleted the status.')

    return redirect(url_for('admin.list_statuses'))


#--------  Team views ----------#

@admin.route('/teams')
@login_required
def list_teams():
    check_admin()
    teams = Team.query.all()
    return render_template('admin/teams/teams.html', teams=teams, title='teams')


@admin.route('/teams/add', methods=['GET', 'POST'])
@login_required
def add_team():
    check_admin()
    add_team = True

    form = TeamForm()
    form.project_id.choices = [(p.id, p.title) for p in Project.query.order_by(text('title'))]
    form.created_by.choices = [(u.id, u.first_name + ' ' + u.last_name) for u in User.query.order_by(text('last_name'), text('first_name'))]
    form.members.choices = [(u.id, u.first_name + ' ' + u.last_name) for u in User.query.order_by(text('last_name'), text('first_name'))]
    team_domain = Domain.query.filter(Domain.name == 'team').first()
    form.status_id.choices = [(s.id, s.name) for s in Status.query.filter(Status.domain_id == team_domain.id).order_by(text('status.name'))]
    default_status = Status.query.filter(Status.domain_id == team_domain.id,
                                         Status.default_for_domain == True).first()
    form.status_id.default = default_status.id
    form.status_id.data = default_status.id
    form.created_by.default = current_user.id
    form.created_by.data = current_user.id
    if form.validate_on_submit():
        team = Team(project_id = form.project_id.data,
                    created_by = form.created_by.data,
                    comment = form.comment.data,
                    vacancies = form.vacancies.data,
                    status_id = form.status_id.data)

        try:
            db.session.add(team)
            db.session.commit()
            db.session.refresh(team)
            for member in form.members.data:
                team_member = TeamMember(team_id=team.id, user_id=member)
                db.session.add(team_member)
            db.session.commit()
            flash('You have successfully added a new team.')
        except:
            flash('Error: team id already exists.')

        return redirect(url_for('admin.list_teams'))

    return render_template('admin/teams/team.html', add_team=add_team,
                           form=form, title='Add team')


@admin.route('/teams/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team(id):
    check_admin()
    add_team = False

    team = Team.query.get_or_404(id)
    form = TeamForm(obj=team)
    form.project_id.choices = [(p.id, p.title) for p in Project.query.order_by(text('title'))]
    form.created_by.choices = [(u.id, u.first_name + ' ' + u.last_name) for u in User.query.order_by(text('last_name'), text('first_name'))]
    form.members.choices = [(u.id, u.first_name + ' ' + u.last_name) for u in User.query.order_by(text('last_name'), text('first_name'))]
    team_domain = Domain.query.filter(Domain.name == 'team').first()
    form.status_id.choices = [(s.id, s.name) for s in Status.query.filter(Status.domain_id == team_domain.id).order_by(text('status.name'))]
    form.members.data = [m.user.id for m in team.members]
    if form.validate_on_submit():
        team.project_id = form.project_id.data
        team.created_by = form.created_by.data
        team.comment = form.comment.data
        team.vacancies = form.vacancies.data
        team.status_id = form.status_id.data
        team.updated_date = datetime.datetime.now()
        db.session.add(team)
        for member in form.members.raw_data:
            if member not in [m.user_id for m in team.members]:
                team_member = TeamMember(team_id=team.id, user_id=member)
                db.session.add(team_member)
        for member in team.members:
            if member.user_id not in form.members.raw_data:
                team_member = TeamMember.query.get(member.id)
                db.session.delete(team_member)
        db.session.commit()
        flash('You have successfully edited the team.')

        return redirect(url_for('admin.list_teams'))

    form.project_id.data = team.project_id
    form.created_by.data = team.created_by
    form.comment.data = team.comment
    form.vacancies.data = team.vacancies
    form.status_id.data = team.status_id
    return render_template('admin/teams/team.html', add_team=add_team,
                           team=team, form=form, title="Edit team")


@admin.route('/teams/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_team(id):
    check_admin()

    team = Team.query.get_or_404(id)
    db.session.delete(team)
    db.session.commit()
    flash('You have successfully deleted the team.')

    return redirect(url_for('admin.list_teams'))


#--------  Transition views ----------#

@admin.route('/transitions')
@login_required
def list_transitions():
    check_admin()
    transitions = Transition.query.all()
    return render_template('admin/transitions/transitions.html', transitions=transitions, title='transitions')


@admin.route('/transitions/add', methods=['GET', 'POST'])
@login_required
def add_transition():
    check_admin()
    add_transition = True

    form = TransitionForm()
    form.from_status_id.choices = [(s.id, s.domain.name + ' - ' + s.name) for s in Status.query.order_by(text('name'))]
    form.to_status_id.choices = [(s.id, s.domain.name + ' - ' + s.name) for s in Status.query.order_by(text('name'))]
    if form.validate_on_submit():
        transition = Transition(from_status_id = form.from_status_id.data,
                                to_status_id = form.to_status_id.data)

        try:
            db.session.add(transition)
            db.session.commit()
            flash('You have successfully added a new transition.')
        except:
            flash('Error: transition id already exists.')

        return redirect(url_for('admin.list_transitions'))

    return render_template('admin/transitions/transition.html', add_transition=add_transition,
                           form=form, title='Add transition')


@admin.route('/transitions/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_transition(id):
    check_admin()
    add_transition = False

    transition = Transition.query.get_or_404(id)
    form = TransitionForm(obj=transition)
    form.from_status_id.choices = [(s.id, s.domain.name + ' - ' + s.name) for s in Status.query.order_by(text('name'))]
    form.to_status_id.choices = [(s.id, s.domain.name + ' - ' + s.name) for s in Status.query.order_by(text('name'))]
    if form.validate_on_submit():
        transition.from_status_id = form.from_status_id.data
        transition.to_status_id = form.to_status_id.data
        db.session.add(transition)
        db.session.commit()
        flash('You have successfully edited the transition.')

        return redirect(url_for('admin.list_transitions'))

    form.from_status_id.data = transition.from_status_id
    form.to_status_id.data = transition.to_status_id

    return render_template('admin/transitions/transition.html', add_transition=add_transition,
                           form=form, title="Edit transition")


@admin.route('/transitions/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_transition(id):
    check_admin()

    transition = Transition.query.get_or_404(id)
    db.session.delete(transition)
    db.session.commit()
    flash('You have successfully deleted the transition.')

    return redirect(url_for('admin.list_transitions'))


#--------  User views ----------#

@admin.route('/users')
@login_required
def list_users():
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html', users=users, title='Users')


@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    check_admin()
    user = User.query.get_or_404(id)

    if user.is_admin:
        abort(403)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.programme = form.programme.data
        user.company = form.company.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned a programme/company.')

        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html',
                           user=user, form=form,
                           title='Assign User')

