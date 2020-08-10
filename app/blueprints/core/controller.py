from flask import (
    request,
    render_template,
    url_for,
    redirect,
    session
)
from flask_login import login_required

from app.blueprints.core.forms import (
    CreateContact,
    CreateOrganisation,
    CreateTicket
)
from app.blueprints.core.models import (
    Contact,
    Organisation,
    Ticket
)
from app.blueprints.user.models import User
from . import core
from werkzeug.exceptions import NotFound



@core.route('/')
def index():
    return render_template('layout/base.html')


@core.route('/contact/create', methods=['GET', 'POST'])
@login_required
def create_contact():
    form = CreateContact(request.form)
    if request.method == 'POST':
        if form.validate():
            form.org_id.data = form.org_id.data.id
            contact = Contact.create(**form.data)
            return render_template('layout/dashboard.html')
    return render_template('core/create_contact.html', form=form)


@core.route('/contact/<con_id>')
@login_required
def view_contact(con_id):
    contact = Contact.query.filter_by(id=con_id).first_or_404()
    columns = [el.name for el in Contact.__table__.columns]
    return render_template('core/view_contact.html', columns=columns, record=contact)


@core.route('/organisation/create', methods=['GET', 'POST'])
@login_required
def create_organisation():
    form = CreateOrganisation(request.form)
    user = User.query.filter_by(name=session['profile']['name']).first_or_404()
    if request.method == 'POST':
        if form.validate():
            org = Organisation.create(
                name=form.name.data,
                address=form.address.data,
                created_by=user.id
            )
            return redirect(url_for('core.create_contact'))
    return render_template('core/create_organisation.html', form=form)


@core.route('/organisation/<org_id>')
@login_required
def view_organisation(org_id):
    org = Organisation.query.filter_by(id=org_id).first_or_404()
    return render_template('core/view_organisation.html', organisation=org)


@core.route('/ticket/create', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = CreateTicket(request.form)
    user = User.query.filter_by(name=session['profile']['name']).first_or_404()

    try:
        org = Organisation.query.filter_by(created_by=user.id).first_or_404()
    except NotFound:
        return redirect(url_for('core.create_organisation'))

    try:
        contact = Contact.query.filter_by(org_id=org.id).first_or_404()
    except NotFound:
        return redirect(url_for('core.create_contact'))

    if request.method == 'POST':
        if form.validate():
            ticket = Ticket.create(
                subject=form.subject.data,
                description=form.description.data,
                severity=form.severity.data,
                status=form.status.data,
                created_by=user.id,
                org_id=org.id,
                contact_id=contact.id
            )
            return redirect(url_for('core.view_organisation', org_id=org.id))
    return render_template('core/create_ticket.html', form=form)
