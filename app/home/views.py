from flask import abort, render_template
from flask_login import current_user, login_required

from app.models import Project
from . import home


@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('home/admin_dashboard.html', title="Dashboard")

@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    projects = Project.query.filter(Project.client_id == current_user.id).all()
    return render_template('home/dashboard.html', projects=projects, title="Dashboard")
