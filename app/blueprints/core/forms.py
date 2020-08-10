from wtforms_alchemy import ModelForm
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.blueprints.core.models import Contact, Organisation, Ticket


def available_organisations():
    return Organisation.query.all()


class CreateOrganisation(ModelForm):
    class Meta:
        model = Organisation


class CreateContact(ModelForm):
    class Meta:
        model = Contact

    org_id = QuerySelectField('Organisation', query_factory=available_organisations, get_label='name')


class CreateTicket(ModelForm):
    class Meta:
        model = Ticket