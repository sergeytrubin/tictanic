from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import (
    SelectField,
    StringField,
    BooleanField,
    TextAreaField)
from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    Regexp,
    ValidationError
)
from wtforms_alchemy import Unique
from wtforms_components import EmailField

from collections import OrderedDict

from app.blueprints.core.models import (
    Contact,
    Organisation,
    Ticket)
import re


def available_organisations():
    return Organisation.query.all()

def validate_phone_number(form, field):
    phoneRegex = re.compile(r'''(
        \+?[0]{0,2}?        # Country Code
        [-.\s]?             # Seperator
        \d{1,3}             # Area/Carrier Code
        [-.\s]?             # Seperator
        \(?\d{1,3}?\)?      # Town Code
        [-.\s]?             # Seperator
        \d{3}               # First 3 digits
        [-.\s]?             # Seperator
        \d{4}               # last digits
    )''', re.VERBOSE)
    if not phoneRegex.search(field.data):
        raise ValidationError('Invalid phone number')



def choices_from_dict(source, prepend_blank=True):
    """
    Convert a dict to a format that's compatible with WTForm's choices. It also
    optionally prepends a "Please select one..." value.

    Example:
      # Convert this data structure:
      STATUS = OrderedDict([
          ('unread', 'Unread'),
          ('open', 'Open'),
          ('contacted', 'Contacted'),
          ('closed', 'Closed')
      ])

      # Into this:
      choices = [('', 'Please select one...'), ('unread', 'Unread) ...]

    :param source: Input source
    :type source: dict
    :param prepend_blank: An optional blank item
    :type prepend_blank: bool
    :return: list
    """
    choices = []

    if prepend_blank:
        choices.append(('', 'Please select one...'))

    for key, value in source.items():
        pair = (key, value)
        choices.append(pair)

    return choices


def choices_from_list(source, prepend_blank=True):
    """
    Convert a list to a format that's compatible with WTForm's choices. It also
    optionally prepends a "Please select one..." value.

    Example:
      # Convert this data structure:
      TIMEZONES = (
        'Africa/Abidjan',
        'Africa/Accra',
        'Africa/Addis_Ababa'
      )

      # Into this:
      choices = [('', 'Please select one...'),
                 ('Africa/Abidjan', 'Africa/Abidjan) ...]

    :param source: Input source
    :type source: list or tuple
    :param prepend_blank: An optional blank item
    :type prepend_blank: bool
    :return: list
    """
    choices = []

    if prepend_blank:
        choices.append(('', 'Please select one...'))

    for item in source:
        pair = (item, item)
        choices.append(pair)

    return choices


class ModelForm(FlaskForm):
    """
    wtforms_components exposes ModelForm but their ModelForm does not inherit
    from flask_wtf's Form, but instead WTForm's Form.

    However, in order to get CSRF protection handled by default we need to
    inherit from flask_wtf's Form. So let's just copy his class directly.

    We modified it by removing the format argument so that wtforms_component
    uses its own default which is to pass in request.form automatically.
    """

    def __init__(self, obj=None, prefix='', **kwargs):
        FlaskForm.__init__(
            self, obj=obj, prefix=prefix, **kwargs
        )
        self._obj = obj


class CreateOrganisation(FlaskForm):
    name = StringField("Please add Organisation Name",
                       [DataRequired(), Length(3, 254)])
    address = TextAreaField("Add Organisation address",
                            [DataRequired(), Length(1, 500)])


class CreateContact(FlaskForm):
    role_choices = ['admin', 'user']

    first_name = StringField("What is your first name?",
                             [DataRequired(), Length(3, 254)])
    last_name = StringField("What is your last name?",
                            [DataRequired(), Length(3, 254)])
    email = EmailField("What's your e-mail address?",
                       [DataRequired(), Length(3, 254)])
    role = SelectField(
        'role',
        validators=[DataRequired()],
        choices=choices_from_list(role_choices)
    )
    mobile = StringField(
        'mobile',
        validators=[validate_phone_number],
    )


# class CreateTicket(ModelForm):
#     class Meta:
#         model = Ticket


class CreateTicket(ModelForm):
    severity_choices = ['Critical', 'High', 'Medium', 'Low']
    status_choices = ['New', 'In progress', 'Closed']

    subject = StringField("Please add a subject",
                       [DataRequired(), Length(3, 254)])
    description = TextAreaField("Describe the issue",
                            [DataRequired(), Length(1, 8192)])
    severity = SelectField(
        'severity',
        validators=[DataRequired()],
        choices=choices_from_list(severity_choices)
    )
    status = SelectField(
        'status',
        validators=[DataRequired()],
        choices=choices_from_list(status_choices)
    )

class SearchForm(FlaskForm):
    q = StringField('Search terms', [Optional(), Length(1, 256)])


class BulkDeleteForm(FlaskForm):
    SCOPE = OrderedDict([
        ('all_selected_items', 'All selected items'),
        ('all_search_results', 'All search results')
    ])

    scope = SelectField('Privileges', [DataRequired()],
                        choices=choices_from_dict(SCOPE, prepend_blank=False))
