from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import ProgrammeForm, CompanyForm, UserAssignForm
from .. import db
from ..models import Programme, Company, User

def check_admin():
    if not current_user.is_admin:
        abort(403)


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

