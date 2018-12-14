from flask import abort, flash, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import and_, or_
from app.models import *


def check_client(project):
    if project.client_id != current_user.id:
        abort(403)


def check_member(team):
    member = TeamMember.query.filter(and_(TeamMember.team_id == team.id, TeamMember.user_id == current_user.id)).first()
    if member is None:
        abort(403)


def check_owner(item):
    if item.user_id != current_user.id:
        abort(403)


def check_members(team, settings):
    if len(team.members) < settings.minimum_team_size:
        return False
    return True


def check_programmes(team):
    programmes = set([m.user.programme_code for m in TeamMember.query.filter(TeamMember.team_id == team.id).all()])
    if len(programmes) > 1:
        return True
    return False


def check_pm(team):
    project_manager = TeamMember.query.filter(and_(TeamMember.team_id == team.id, TeamMember.project_manager == True)).first()
    if project_manager:
        return True
    return False


def get_status(domain_name, status_name):
    domain = Domain.query.filter(Domain.name == domain_name).first()
    return Status.query.filter(and_(Status.domain==domain, Status.name==status_name)).first()


def get_bids(project):
    return Team.query.filter(and_(Team.project_id == project.id)).join(Status).\
                      filter(or_(Status.name=='Submitted', Status.name=='Accepted', Status.name=='Shortlisted')).all()


def get_new_teams(project):
    return Team.query.filter(and_(Team.project_id == project.id)).join(Status).\
                      filter(Status.name=='New').all()


def delete_notes(user_id, project_id=None):
    if project_id is None:
        notes = Interest.query.filter(Interest.user_id == user_id).all()
    else:
        notes = Interest.query.filter(and_(Interest.user_id == user_id, Interest.project_id == project_id)).all()
    for note in notes:
        db.session.delete(note)


def delete_flags(user_id, project_id=None):
    if project_id is None:
        flags = Flag.query.filter(Flag.user_id == user_id).all()
    else:
        flags = Flag.query.filter(and_(Flag.user_id == user_id, Flag.project_id == project_id)).all()
    for flag in flags:
        db.session.delete(flag)


def alert(id, code, team=False, project=None):
    message = AlertText.query.get_or_404(code)
    text = message.message_text

    if "{project}" in text:
        text = text.replace("{project}", "'"+project.title+"'")
    if "{client}" in text:
        text = text.replace("{client}", project.client.first_name + ' ' + project.client.last_name)
    if "{client_email}" in text:
        text = text.replace("{client_email}", project.client.email)

    if team:
        recipients = [m.user for m in TeamMember.query.filter(TeamMember.team_id == id).all()]
    else:
        recipients = User.query.filter(User.id==id).all()

    for recipient in recipients:
        queued = AlertQueue(
            user_id = recipient.id,
            email = recipient.email,
            subject = message.subject,
            message_text = text
        )
        db.session.add(queued)
        db.session.commit()

