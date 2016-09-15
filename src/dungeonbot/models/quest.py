# from flask_sqlalchemy import SQLAlchemy
# from dungeonbot import app
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound


# db = SQLAlchemy(app)

from dungeonbot.models import db


class QuestModel(db.Model):
    """Model for the Quest object, largely copied from KarmaModel."""
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    description = db.Column(db.String(2048))
    quest_giver = db.Column(db.String(256))
    location_given = db.Column(db.String(256))
    status = db.Column(db.Boolean)
    created = db.Column(db.DateTime, nullable=False,
                        default=datetime.now())
    last_updated = db.Column(db.DateTime, nullable=False,
                             default=datetime.now())
    completed_date = db.Column(db.DateTime)

    @classmethod
    def new(cls, title=None, description=None, quest_giver=None,
            location_given=None, session=None):
        if session is None:
            session = db.session

        instance = cls(
            title=title,
            description=description,
            quest_giver=quest_giver,
            location_given=location_given,
            status=True,
            completed_date=None
        )

        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def modify(cls, quest_id, title=None, description=None, quest_giver=None,
               location=None, session=None):
        if session is None:
            session = db.session

        instance = cls.get_by_id(quest_id)

        if title:
            instance.title = title

        if description:
            instance.description = description

        if quest_giver:
            instance.quest_giver = quest_giver

        if location:
            instance.location_given = location

        instance.last_updated = datetime.now()

        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def add_detail(cls, quest_id, more_detail=None, session=None):
        if session is None:
            session = db.session

        instance = cls.get_by_id(quest_id, session)

        if more_detail:
            longer_desc = "{}||{}"
            if instance.description:
                instance.description = longer_desc.format(
                    instance.description, more_detail)
            else:
                instance.description = more_detail
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
    def list_active(cls, how_many=5, session=None):
        if session is None:
            session = db.session
        return session.query(cls.id, cls.title, cls.created).order_by('id').filter_by(status=True).limit(how_many).all()

    @classmethod
    def list_inactive(cls, session=None):
        if session is None:
            session = db.session
        return session.query(cls.id, cls.title, cls.completed_date).order_by('completed_date').filter_by(status=False).all()

    @classmethod
    def list_all(cls, session=None):
        if session is None:
            session = db.session
        return session.query(cls.id, cls.title, cls.created, cls.status).order_by('created desc').all()

    @classmethod
    def get_by_id(cls, quest_id=None, session=None):
        if session is None:
            session = db.session
        # import pdb; pdb.set_trace()

        try:
            instance = session.query(cls).filter_by(id=quest_id).one()
        except NoResultFound:
            instance = None
        return instance

        # return session.query(cls.id, cls.title, cls.description, cls.quest_giver, cls.location_given, cls.status, cls.created, cls.last_updated, cls.completed_date).filter_by(id=quest_id).first()

    @classmethod
    def get_by_name(cls, quest_name=None, session=None):
        if session is None:
            session = db.session
        try:
            instance = session.query(cls).filter_by(
                title=quest_name).one()
        except NoResultFound:
            instance = None
        return instance

    @property
    def json(self):
        return {
            "id": self.id,
            "title": self.title.title(),
            "description": self.description,
            "quest_giver": self.quest_giver,
            "location_given": self.location_given,
            "status": self.status,
            "created": self.created,
            "last_updated": self.last_updated,
            "completed_date": self.completed_date,
        }

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
            self.description,
            self.quest_giver,
            self.location_given,
            self.status,
            self.created,
            self.last_updated,
            self.completed_date,
        )
