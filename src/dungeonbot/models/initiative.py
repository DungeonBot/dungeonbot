from dungeonbot.models import db
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


class InitiativeModel(db.Model):
    """Initiative Model."""

    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    init = db.Column(db.SmallInteger)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    @classmethod
    def set(cls, name=None, init=None, session=None):
        """Create a new entity with an initiative value in the DB."""
        if session is None:
            session = db.session
        try:
            instance = cls(name=name, init=init)
            session.add(instance)
            session.commit()
            return instance
        except IntegrityError:
            session.rollback()
            return "duplicate"

    @classmethod
    def get(cls, name=None, session=None):
        """Retrieve initiative by entity name."""
        if session is None:
            session = db.session
        try:
            instance = session.query(cls).filter_by(name=name).one()
        except NoResultFound:
            instance = None
        return instance

    @classmethod
    def list(cls, session=None):
        """List all entities in current initiative order."""
        if session is None:
            session = db.session
        return session.query(cls).order_by('init desc').all()

    @classmethod
    def delete(cls, name=None, session=None):
        """Delete entry by entity name."""
        if session is None:
            session = db.session
        try:
            instance = session.query(cls).filter_by(name=name).one()
            session.delete(instance)
            session.commit()
            return instance
        except NoResultFound:
            return None

    @classmethod
    def clear(cls, session=None):
        """Delete all initiative entries."""
        if session is None:
            session = db.session
        instances = session.query(cls).all()
        for instance in instances:
            session.delete(instance)
            session.commit()

