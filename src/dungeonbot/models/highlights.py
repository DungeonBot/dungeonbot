from dungeonbot.models import db
from datetime import datetime


class HighlightModel(db.Model):
    """Model for campaign highlights."""

    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(256))
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    @classmethod
    def new(cls, args=None, session=None):
        """Create and store new Highlight."""
        if not args:
            return
        if session is None:
            session = db.session
        instance = cls(text=args)
        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def list(cls, how_many=10, session=None):
        """Retrieve stored highlights, limited by 'how_many'."""
        if session is None:
            session = db.session
        return (
            session.query(cls).
            order_by('created desc').
            limit(how_many).
            all()
        )
