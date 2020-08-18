from flask import (
    request,
    render_template,
    url_for,
    redirect,
    session,
    flash
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
    form = CreateContact()
    if request.method == 'POST' and form.validate():
        org = Organisation.query.filter_by(
            created_by=User.get_id(session)).first()
        try:
            Contact.create(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                mobile=request.form['mobile'],
                role=request.form['role'],
                org_id=org.id,
                created_by=User.get_id(session)
            )
        except Exception as err:
            print(err)
        return redirect(url_for('core.create_ticket'))
    return render_template('core/create_contact.html', form=form)


@core.route('/contact/<con_id>')
@login_required
def view_contact(con_id):
    contact = Contact.query.filter_by(id=con_id).first_or_404()
    columns = [el.name for el in Contact.__table__.columns]
    return render_template(
        'core/view_contact.html',
        columns=columns,
        record=contact
    )


@core.route('/organisation/create', methods=['GET', 'POST'])
@login_required
def create_organisation():
    form = CreateOrganisation()
    if request.method == 'POST' and form.validate():
        Organisation.create(
            name=request.form['name'],
            address=request.form['address'],
            created_by=User.get_id(session)
        )
        flash('organisation created', 'success')
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
    form = CreateTicket()
    user_id = User.get_id(session)

    try:
        org = Organisation.query.filter_by(created_by=user_id).first_or_404()
    except NotFound:
        return redirect(url_for('core.create_organisation'))

    try:
        contact = Contact.query.filter_by(org_id=org.id).first_or_404()
    except NotFound:
        return redirect(url_for('core.create_contact'))

    if request.method == 'POST' and form.validate():
            Ticket.create(
                subject=request.form['subject'],
                description=request.form['description'],
                severity=request.form['severity'],
                status=request.form['status'],
                created_by=user_id,
                org_id=org.id,
                org_name=org.name,
                org_address=org.address,
                contact_id=contact.id,
                contact_name=f"{contact.first_name} {contact.last_name}",
                contact_email=contact.email,
                contact_phone=contact.mobile
            )
            flash('Thank you! The ticket was created', 'success')
            return redirect(url_for('core.view_tickets'))
    return render_template('core/create_ticket.html', form=form)


@core.route('/tickets')
def view_tickets():
    user_id = User.get_id(session)

    tickets = Ticket.query.filter_by(created_by=user_id).all()
    print(tickets)
    return render_template('core/view_tickets.html', tickets=tickets)
