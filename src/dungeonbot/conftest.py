"""Configure base testing class for all other test classes."""

from dungeonbot import app
from dungeonbot.models import db

from flask_testing import TestCase

import os


class BaseTest(TestCase):
    """The base class that any test hitting the db will use."""

    TESTING = True

    def create_app(self):
        """Create an app configured for testing."""
        if os.getenv("DB_URL"):
            dburi = os.getenv("DB_URL")
        else:
            dburi = app.config["SQLALCHEMY_DATABASE_URI"].split("/")
            dburi[-1] = "dungeonbot_test"
            dburi = "/".join(dburi)

        app.config.update(SQLALCHEMY_DATABASE_URI=dburi)

        return app

    def setUp(self):
        """Setup the test DB before any tests."""
        db.create_all()
        self.db = db

    def tearDown(self):
        """Destroy the test database."""
        self.db.session.remove()
        self.db.drop_all()
