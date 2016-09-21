#!/usr/bin/env python

"""Manage the Flask project.

Provides functionality for performing database oeprations (init,
migrate, upgrade), running the project locally, and creating a shell
entrypoint pre-populated with key aspects of the project.

"""
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand

from dungeonbot import app
from dungeonbot import models
from dungeonbot.models import (
    karma,
    quest,
    roll,
	attribute
)
import os
import subprocess


def _make_context():
    return dict(
        app=app,
        db=models.db,
        models=[
            karma,
            quest,
            roll,
        ],
    )

manager = Manager(app)

manager.add_command("runserver", Server(host="0.0.0.0", port=5006))
manager.add_command("shell", Shell(make_context=_make_context))

migrate = Migrate(app, models.db)
manager.add_command("db", MigrateCommand)


@manager.command
def test():
    """Run testing suite."""
    cmd = "py.test -v --cov=dungeonbot --cov-report=term-missing"

    print(
        """
Running test suite with command:
{}

###############################################################################
NOTE

Do not use 'manage.py test' when testing in CI, or in any other script which
requires the detection of a nonzero exit status to signify that the tests have
failed. Instead, use the above command directly.

Any nonzero (=failing) exit status of the 'py.test' process will be swallowed
by the wrapping 'manage.py test' Python process, which will return a zero
(=successful) status unless a Python exception occurs. The tests will fail,
but the exit status of 'manage.py test' will say that everything is fine.

Compare for yourself, using 'echo $?' to grab the most recent exit status (make
sure there is at least one failing test in the test suite):

$  {} ; echo $?

vs

$  python manage.py test ; echo $?
###############################################################################
""".format(cmd, cmd)
    )

    os.system(cmd)


if __name__ == '__main__':
    manager.run()
