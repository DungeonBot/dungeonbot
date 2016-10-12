from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from dungeonbot.models import db
from datetime import datetime


class RollModel(db.Model):
    """Model for saved rolls.

    Saved rolls will have a string id key, identifying name of roll.
    Saved rolls will also have a roll_str property -- the value for the
    roll.
    """

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), unique=True)
    val = db.Column(db.String(256))
    user = db.Column(db.String(256))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    @classmethod
    def new(cls, key="", val="", user=None, session=None):
        """Create New saved roll from a key value pair."""
        if session is None:
            session = db.session
        if not key or not val:
            return None
        try:
            instance = cls(key=key, val=val, user=user["id"])
            session.add(instance)
            session.commit()
            return instance
        except IntegrityError:
            session.rollback()
            return "duplicate"

    @classmethod
    def get(cls, key=None, user=None, session=None):
        """Query Database by name (Key)."""
        if session is None:
            session = db.session
        try:
            instance = session.query(cls).filter_by(key=key, user=user["id"]).one()
        except NoResultFound:
            instance = None
        return instance

    @classmethod
    def delete(cls, instance, session=None):
        """Delete Roll."""
        if session is None:
            session = db.session
        if not isinstance(instance, RollModel):
            return None
        name = instance.key
        session.delete(instance)
        session.commit()
        return name

    @classmethod
    def list(cls, how_many=10, user=None, session=None):
        """List saved rolls, defaults to 10 most recent."""
        if session is None:
            session = db.session
        return(
            session.query(cls).
            filter_by(user=user["id"]).
            order_by('created desc').
            limit(how_many).
            all()
        )

    @property
    def json(self):
        """Return JSON representation of model."""
        return {
            "id": self.id,
            "key": self.key,
            "value": self.val,
            "user": self.user
        }

    @property
    def slack_msg(self):
        """Return slack msg."""
        return "{}: {}".format(self.key, self.val)

    def __repr__(self):
        """Repr."""
        return(
            """
            <dungeonbot.models.RollModel(id={},key={}, value={}, user={})>
            """.format(self.id, self.key, self.val, self.user))
