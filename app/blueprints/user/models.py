from sqlalchemy_utils import EmailType
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.exc import IntegrityError
from app.database import db
from app.blueprints.core import Base
from app.extensions import bcrypt
from app.lib.util_sqlalchemy import ResourceMixin, AwareDateTime

class User(Base):

    __tablename__ = 'user'

    username = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(EmailType, nullable=False, info={"label": "Email"})
    image_link = db.Column(db.String(500), nullable=False)

    @classmethod
    def find_by_identity(cls, identity):
        return User.query.filter(
            (User.email == identity) | (User.username == identity)).first()

    @staticmethod
    def create(**kwargs):
        u = User(**kwargs)
        db.session.add(u)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
        return u
