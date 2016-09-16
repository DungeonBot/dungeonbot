from dungeonbot.models import db
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound


class AttrModel(db.Model):
    """Attribute Model."""

    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), unique=True)
    val = db.Column(db.String(256))
    user = db.Column(db.String(256))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    @classmethod
    def set(cls, args=None, user=None, session=None):
        """Create a new Attribute Key/Val pair in DB."""
        # need to delimit between key and value
        if session is None:
            session = db.session
        key, val = args
        # try:
        instance = cls(key=key, val=val, user=user)
        session.add(instance)
        session.commit()
        return instance
        # except IntegrityError:
        # return "{} already exists".format(args)

    @classmethod
    def get(cls, args=None, user=None, session=None):
        """Retrieve Attribute by key for the requesting user."""
        if session is None:
            session = db.session
        try:
            instance = session.query(cls).filter_by(key=args[0], user=user).one()
        except NoResultFound:
            instance = None
        return instance

    @classmethod
    def list(cls, args=None, user=None, session=None):
        """List saved attributes for requesting user.

        Defaults to the ten most recent, but optional arg can
        be passed to raise or lower the limit.
        """
        if session is None:
            session = db.session
        how_many = int(args[0]) if len(args) > 0 else 10
        return session.query(cls).order_by('created desc').limit(how_many).all()

    @classmethod
    def delete(cls, args, user=None, session=None):
        """Delete attribute by key belonging to requesting user."""
        if session is None:
            session = db.session
        try:
            instance = session.query(cls).filter_by(key=args[0], user=user).one()
            session.delete(instance)
            session.commit()
            return "Successfully deleted {}".format(args)
        except NoResultFound:
            return "No entry named {} found".format(args)
