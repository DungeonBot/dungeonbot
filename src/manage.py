#!/usr/bin/env python

from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

from dungeonbot import app
from dungeonbot import models

from dungeonbot.models import (
    karma,
    roll,
    quest,
)

import os


def _make_context():
    return dict(app=app, db=models.db, models=models)

manager = Manager(app)

manager.add_command("runserver", Server(host="0.0.0.0", port=5006))
manager.add_command("shell", Shell(make_context=_make_context))

migrate = Migrate(app, models.db)
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    """Run testing suite."""
    os.system("py.test -v --cov=dungeonbot --cov-report=term-missing")


if __name__ == '__main__':
    manager.run()
