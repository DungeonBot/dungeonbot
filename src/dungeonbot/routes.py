import os

from flask import (
    render_template,
    request,
    Response
)

from threading import Thread

from dungeonbot import app
from dungeonbot.oauth import token_negotiation
from dungeonbot.handlers.event import EventHandler
from auxiliaries.helpers import eprint


################################
# TOOLS
################################

def event_is_important(event):
    suffixes = ["++", "--"]
    if (event['user'] != os.getenv("BOT_ID")) and \
       (
            event['text'][0] == "!" or
            event['text'][-2:] in suffixes
       ):
        return True
    return False


def process_important_event(event=None):
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
    eprint("hit / route")

    if request.method == "GET":
        return render_template("index.html")

    event = request.json['event']
    event['team_id'] = request.json['team_id']

    thread = Thread(target=process_important_event, kwargs={"event": event})
    thread.start()

    return Response(status=200)


@app.route("/oauth", methods=["GET", "POST"])
def oauth():
    eprint("hit /oauth route")

    return token_negotiation()
