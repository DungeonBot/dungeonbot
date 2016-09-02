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
        return session.query(cls).order_by('created desc').limit(how_many).all()

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


class QuestModel(db.Model):

    """Model for the Quest object, largely copied from KarmaModel."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.String(1024))
    quest_giver = db.Column(db.String(1024))
    location_given = db.Column(db.String(1024))
    status = db.Column(db.Boolean)
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.now())
    last_updated = db.Column(db.DateTime, nullable=False,
                             default=datetime.now())
    completed_date = db.Column(db.DateTime)

    @classmethod
    def new(cls, title=None, description=None, quest_giver=None,
            location_given=None, status=True, completed_date=None,
            session=None):
        if session is None:
            session = db.session

        instance = cls(
            title=title,
            description=description,
            quest_giver=quest_giver,
            location_given=location_given,
            status=status,
            completed_date=None
        )

        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def modify(cls, quest_id, title=None, description=None,
               session=None):
        if session is None:
            session = db.session

        instance = cls.get_by_id(quest_id)

        if title:
            instance.title = title

        if description:
            instance.description = description

        instance.last_updated = datetime.now()

        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def add_detail(cls, quest_id, more_detail=None):
        if session is None:
            session = db.session

        instance = cls.get_by_id(quest_id)
        longer_desc = """{}

{}
"""
        instance.description = longer_desc.format(
            instance.description, more_detail)
        instance.last_updated = datetime.now()

        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def complete(cls, quest_id=None, session=None):
        if session is None:
            session = db.session

        instance = cls.get_by_id(quest_id)
        instance.last_updated = datetime.now()
        instance.completed_date = datetime.now()
        instance.status = False

        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def list_newest(cls, how_many=5, session=None):
        if session is None:
            session = db.session
        return session.query(cls.id, cls.title, cls.created).order_by('created desc').limit(how_many).all()

    @classmethod
    def list_last_updated(cls, how_many=5, session=None):
        if session is None:
            session = db.session
        return session.query(cls.id, cls.title, cls.last_updated).order_by('last_updated desc').limit(how_many).all()

    @classmethod
    def list_active(cls, session=None):
        if session is None:
            session = db.session
        return session.query(cls.id, cls.title).order_by('created desc').filter_by(status=True).all()

    @classmethod
    def list_inactive(cls, session=None):
        if session is None:
            session = db.session
        return session.query(cls.id, cls.title, cls.completed_date).order_by('completed_date').filter_by(status=False).all()

    @classmethod
    def get_by_id(cls, quest_id=None, session=None):
        if session is None:
            session = db.session
        return session.query(cls).get(quest_id)

    @classmethod
    def get_by_name(cls, quest_name=None, session=None):
        if session is None:
            session = db.session
        try:
            instance = session.query(cls).filter_by(
                quest_name=quest_name).one()
        except NoResultFound:
            instance = None
        return instance

    @property
    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "quest_giver": self.quest_giver,
            "location_given": self.location_given,
            "status": self.status,
            "created": self.created,
            "last_updated": self.last_updated,
            "completed_date": self.completed_date,
        }

    @property
    def slack_msg(self):
        output = """```
*Quest #{}: {}*
-----------------------
{}

_Given By {} in {}_

_Date Added: {}_
_Last Updated: {}_
*Status: {}*
```"""
        status = "Active" if self.status else "Inactive"

        return output.format(
            self.id,
            self.title,
            self.description,
            self.quest_giver,
            self.location_given,
            self.created,
            self.last_updated,
            status
        )

    def __repr__(self):
        return (
            "<dungeonbot.models.QuestModel(" +
            "id={}, description={}, quest_giver={}, " +
            "location_given={}, status={}, created={}, " +
            "last_updated={}, completed_date={}"
            ") [id: {}, description: {}, quest_giver: {}, " +
            "location_given: {}, status: {}, created: {}, " +
            "last_updated: {}, completed_date: {}]>"
        ).format(
            self.id,
            self.title,
            self.upvotes,
            self.quest_giver,
            self.location_given,
            self.status,
            self.downvotes,
            self.karma,
            self.created,
        )
