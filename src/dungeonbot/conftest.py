from dungeonbot import app

from flask_testing import TestCase


class BaseTest(TestCase):
    """The base class that any test hitting the db will use."""

    TESTING = True

    def create_app(self):
        """Need to update the app's database URI to point to the testdb.

        Note, the test db must be created first!
        """
        dburi = app.config["SQLALCHEMY_DATABASE_URI"].split("/")
        dburi[-1] = "dungeonbot_test"
        dburi = "/".join(dburi)

        app.config.update(SQLALCHEMY_DATABASE_URI=dburi)
        _app = app

        return _app

    def setUp(self):
        """Setup the test DB before any tests."""
        from dungeonbot.models import db
        db.create_all()
        self.db = db

    def tearDown(self):
        """Destroy the test database."""
        self.db.session.remove()
        self.db.drop_all()
