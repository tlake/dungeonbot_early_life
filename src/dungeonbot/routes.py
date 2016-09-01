import os

from flask import (
    render_template,
    request,
    Response
)

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

    if event_is_important(event):
        eprint("event considered important:")
        eprint(event)

        handler = EventHandler(event)
        handler.process_event()

    else:
        eprint("event not considered important:")
        eprint(event)

    return Response(status=200)


@app.route("/oauth", methods=["GET", "POST"])
def oauth():
    eprint("hit /oauth route")

    return token_negotiation()
