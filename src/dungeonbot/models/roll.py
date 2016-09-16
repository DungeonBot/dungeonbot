from sqlalchemy.orm.exc import NoResultFound
from dungeonbot.models import db


class RollModel(db.Model):
    """Model for saved rolls.

    Saved rolls will have a string id key, identifying name of roll.
    Saved rolls will also have a roll_str property -- the value for the
    roll.
    """

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256))
    val = db.Column(db.String(256))
    user = db.Column(db.String(256))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    @classmethod
    def parse_key_val_pairs(cls, roll_str):
        """Parse Key/Val Pairs from a string, where val begins with an Integer."""
        import re
        m = re.search("\d", roll_str)
        if m:
            idx = m.start()
            key = roll_str[:idx]
            value = roll_str[idx:]
            return key, value

    @classmethod
    def new(cls, key="", val="", user=None, session=None):
        """Create New saved roll from a key value pair."""
        if session is None:
            session = db.session
        instance = cls(key=key, val=val, user=user)
        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def get_by_key(cls, key=None, user=None, session=None):
        """Query Database by name (Key)."""
        if session is None:
            session = db.session
        try:
            instance = session.query(cls).filter_by(key=key, user=user).one()
        except NoResultFound:
            instance = None
        return instance

    @classmethod
    def list(cls, how_many=10, user=None, session=None):
        """List saved rolls, defaults to 10 most recent."""
        if session is None:
            session = db.session
        return session.query(cls).filter_by(user=user).order_by('created desc').limit(how_many).all()

    @property
    def json(self):
        """Return JSON representation of model."""
        return {"id": self.id, "key": self.key, "value": self.value, "user": self.user}

    @property
    def slack_msg(self):
        """Return slack msg."""
        return "{}: {}".format(self.key, self.value)

    @property
    def repr(self):
        """Repr."""
        return(
            """
            <dungeonbot.models.RollModel(id={},key={}, value={}, user={})>
            """.format(self.id, self.key, self.value, self.user))
