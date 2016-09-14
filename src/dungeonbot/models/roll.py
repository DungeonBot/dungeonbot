from dungeonbot.models import db


class RollModel(db.model):
    """Model for saved rolls.

    Saved rolls will have a string id key, identifying name of roll.
    Saved rolls will also have a roll_str property -- the value for the
    roll.
    """

    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True)
    string_id = db.Column(db.String(256))
