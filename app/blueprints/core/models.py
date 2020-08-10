from sqlalchemy_utils import EmailType, ChoiceType
from app.database import db
from app.lib.util_sqlalchemy import ResourceMixin, AwareDateTime
from app.lib.util_datetime import tzware_datetime
from sqlalchemy.exc import IntegrityError



class Base(db.Model, ResourceMixin):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(AwareDateTime(),
                            default=tzware_datetime)
    date_modified = db.Column(AwareDateTime(),
                              default=tzware_datetime,
                              onupdate=tzware_datetime)


class Contact(Base):

    """User input fields - these fields can be set by user and are included in forms"""
    first_name = db.Column(db.String(60), nullable=False, info={"label": "First Name"})
    last_name = db.Column(db.String(60), nullable=False, info={"label": "Last Name"})
    email = db.Column(EmailType, nullable=False, info={"label": "Email"})
    mobile = db.Column(db.Integer, info={"label": "Mobile"})
    role = db.Column(db.String(60), info={"label": "Role"})
    org_id = db.Column(db.Integer, db.ForeignKey('organisation.id', ondelete='cascade'), info={"label": "Organisation"})
    created_by = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'))

    activities = db.relationship('Activity', backref='contact')

    @staticmethod
    def create(**kwargs):
        c = Contact(**kwargs)
        db.session.add(c)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return c


class Organisation(Base):

    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text())

    created_by=db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'))

    contacts = db.relationship('Contact', backref='organisation')
    activities = db.relationship('Activity', backref='contact_lookup')

    @staticmethod
    def create(**kwargs):
        o = Organisation(**kwargs)
        db.session.add(o)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return o


class Ticket(Base):
    STATUS_CHOICE = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ]

    SEV_CHOICE = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low')
    ]
    subject = subject = db.Column(db.String(250), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    severity = db.Column(ChoiceType(SEV_CHOICE), nullable=False)
    status = db.Column(ChoiceType(STATUS_CHOICE), nullable=False)
    close_date = db.Column(AwareDateTime(),
                       onupdate=tzware_datetime)
    created_by=db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'))
    org_id=db.Column(db.Integer, db.ForeignKey('organisation.id', ondelete='cascade'))
    contact_id=db.Column(db.Integer, db.ForeignKey('contact.id', ondelete='cascade'))

    activities = db.relationship('Activity', backref='ticket')

    @staticmethod
    def create(**kwargs):
        t = Ticket(**kwargs)
        db.session.add(t)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return t


class Invoice(Base):

    issue_date = db.Column(db.Date)
    amount = db.Column(db.Integer, nullable=False)
    paid = db.Column(db.Boolean, default=False)

    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))


class Activity(Base):

    subject = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.String)

    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'))
    org_id = db.Column(db.Integer, db.ForeignKey('organisation.id', ondelete='cascade'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id', ondelete='cascade'))
