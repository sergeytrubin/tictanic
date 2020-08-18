from sqlalchemy import or_
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
    mobile = db.Column(db.String(60), info={"label": "Mobile"})
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
        except Exception as err:
            db.session.rollback()
            print('ERROR ERROR ERROR')
            print(err)
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
        except Exception as err:
            db.session.rollback()
            print('ERROR ERROR ERROR')
            print(err)
        return o


class Ticket(Base):

    subject = db.Column(
        db.String(250), nullable=False,info={"label": "Subject"})
    description = db.Column(
        db.Text(), nullable=False, info={"label": "Description"})
    severity = db.Column(
        db.String(250), nullable=False,info={"label": "Severity"})
    status = db.Column(
        db.String(250), nullable=False, info={"label": "Status"})
    close_date = db.Column(
        AwareDateTime(),onupdate=tzware_datetime)
    created_by=db.Column(
        db.Integer,db.ForeignKey('user.id', ondelete='cascade'))
    org_id=db.Column(
        db.Integer, db.ForeignKey('organisation.id', ondelete='cascade'))
    org_name = db.Column(db.String(250), nullable=False)
    org_address = db.Column(db.Text(), nullable=False)
    contact_id=db.Column(
        db.Integer, db.ForeignKey('contact.id', ondelete='cascade'))
    contact_name = db.Column(
        db.String(250), nullable=False, info={"label": "Full Name"})
    contact_email = db.Column(
        EmailType, nullable=False, info={"label": "Email"})
    contact_phone = db.Column(
        db.String(250), nullable=False, info={"label": "Phone"})

    activities = db.relationship('Activity', backref='ticket')

    def short(self):
        return {
            'id': self.id,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'subject': self.subject,
            'severity': self.severity,
            'status': self.status,
            'closed_date': self.close_date
        }

    def long(self):
        return {
            'id': self.id,
            'date_created': self.date_created,
            'date_modified': self.date_modified,
            'subject': self.subject,
            'description': self.description,
            'severity': self.severity,
            'status': self.status,
            'closed_date': self.close_date,
            'created_by': self.created_by,
            'org_id': self.org_id,
            'contact_id': self.contact_id
        }

    @staticmethod
    def create(**kwargs):
        t = Ticket(**kwargs)
        db.session.add(t)
        try:
            db.session.commit()
        except Exception as err:
            db.session.rollback()
            print('ERROR ERROR ERROR')
            print(err)
        return t

    @classmethod
    def search(cls, query):
        """
        Search a resource by 1 or more fields.

        :param query: Search query
        :type query: str
        :return: SQLAlchemy filter
        """
        if not query:
            return ''

        search_query = f'%{query}%'
        search_chain = (Ticket.subject.ilike(search_query),
                        Ticket.description.ilike(search_query),
                        Ticket.status.ilike(search_query),
                        Ticket.severity.ilike(search_query))

        return or_(*search_chain)



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
