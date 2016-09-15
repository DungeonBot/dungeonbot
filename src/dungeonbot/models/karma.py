from dungeonbot.models import db

from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound


class KarmaModel(db.Model):
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    string_id = db.Column(db.String(256))
    upvotes = db.Column(db.Integer)
    downvotes = db.Column(db.Integer)
    karma = db.Column(db.Integer)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    @classmethod
    def new(cls, string_id=None, upvotes=0, downvotes=0, session=None):
        if session is None:
            session = db.session
        instance = cls(
            string_id=string_id,
            upvotes=upvotes,
            downvotes=downvotes,
            karma=(upvotes - downvotes),
        )
        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def modify(cls, string_id=None, upvotes=0, downvotes=0, session=None):
        if session is None:
            session = db.session
        instance = cls.get_by_name(string_id)
        instance.upvotes += upvotes
        instance.downvotes += downvotes
        instance.karma = (instance.upvotes - instance.downvotes)
        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def get_by_name(cls, string_id=None, session=None):
        if session is None:
            session = db.session
        try:
            instance = session.query(cls).filter_by(string_id=string_id).one()
        except NoResultFound:
            instance = None
        return instance

    @classmethod
    def get_by_id(cls, model_id=None, session=None):
        if session is None:
            session = db.session
        return session.query(cls).get(model_id)

    @classmethod
    def list_newest(cls, how_many=5, session=None):
        if session is None:
            session = db.session
        return (
            session.query(cls).
            order_by('created desc').
            limit(how_many).
            all()
        )

    @classmethod
    def list_highest(cls, how_many=5, session=None):
        if session is None:
            session = db.session
        return session.query(cls).order_by('karma desc').limit(how_many).all()

    @classmethod
    def list_lowest(cls, how_many=5, session=None):
        if session is None:
            session = db.session
        return session.query(cls).order_by('karma').limit(how_many).all()

    @property
    def json(self):
        return {
            "id": self.id,
            "string_id": self.string_id,
            "upvotes": self.upvotes,
            "downvotes": self.downvotes,
            "karma": self.karma,
            "created": self.created,
        }

    @property
    def slack_msg(self):
        return "*{}* has *{}* karma _({} ++, {} --)_".format(
            self.string_id,
            self.karma,
            self.upvotes,
            self.downvotes,
        )

    def __repr__(self):
        return (
            "<dungeonbot.models.KarmaModel(" +
            "string_id={}, upvotes={}, downvotes={}" +
            ") [id: {}, karma: {}, created: {}]>"
        ).format(
            self.string_id,
            self.upvotes,
            self.downvotes,
            self.id,
            self.karma,
            self.created,
        )
