from flask_sqlalchemy import SQLAlchemy
from dungeonbot import app


db = SQLAlchemy(app)


class RollModel(db.model):
    """Model for saved rolls.

    Saved rolls will have a string id key, identifying name of roll.
    Saved rolls will also have a roll_str property -- the value for the
    roll.
    """

    id = db.Column(db.Integer, primary_key=True)
    string_id = db.Column(db.String(256))
