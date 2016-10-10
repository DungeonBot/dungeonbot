"""Define API routes."""

import os

from flask import (
    request,
    redirect,
    Response,
)

from threading import Thread

from dungeonbot import app
from dungeonbot.handlers.event import EventHandler
from auxiliaries.helpers import eprint


################################
# TOOLS
################################

def event_is_important(event):
    """Assert event is valid command and not posted by dungeonbot."""
    suffixes = ["++", "--"]

    if (
        event['user'] != os.getenv("BOT_ID") and
        (
            event['text'][0] == "!" or
            event['text'][-2:] in suffixes
        )
    ):
        return True

    return False


def process_event(event=None):
    """Process event.

    If the event sent by Slack's Events API is something that we
    consider important and that should be acted upon, spin up an
    EventHandler to handle that event.

    """
    eprint("Thread started!")
    eprint("Event obtained:", event)

    if event_is_important(event):
        eprint("event considered important:")
        eprint(event)

        handler = EventHandler(event)
        handler.process_event()

    else:
        eprint("event not considered important:")
        eprint(event)


################################
# API ROUTES
################################

@app.route("/", methods=["GET", "POST"])
def root():
    """Define the root route.

    This is where Slack's Events API sends all of the events that
    dungeonbot is subscribed to as POST requests.

    Additionally, when accessed by a GET request, this route simply
    redirects to the readme file in master branch of the repository.

    """
    eprint("hit / route")

    if request.method == "GET":
        return redirect(
            "http://gitlab.com/tannerlake/dungeonbot/blob/master/README.md",
            code=302
        )

    event = request.json['event']
    event['team_id'] = request.json['team_id']

    thread = Thread(target=process_event, kwargs={"event": event})
    thread.start()

    return Response(status=200)


@app.route("/oauth", methods=["GET", "POST"])
def oauth():
    """Define OAuth route for adding dungeonbot to Slack teams."""
    eprint("hit /oauth route")

    return Response(status=200)
