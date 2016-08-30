# -*- coding: utf-8 -*-

from flask import (
    Flask,
    render_template,
    request,
    Response
)

from dungeonbot.oauth import token_negotiation
from dungeonbot.handlers import EventHandler

import os

from auxiliaries.helpers import eprint


################################
# APP SETTINGS
#################################

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_CRED = DB_USER + ":" + DB_PASS
DB_NAME = "dungeonbot_db"
DB_URL = "postgresql://" + DB_CRED + "@localhost/" + DB_NAME

app = Flask(__name__)
app.config.update(
    DEBUG=os.getenv("DEBUG", False),
    SECRET_KEY=os.getenv("SECRET_KEY", "sooper seekrit"),
    SQLALCHEMY_DATABASE_URI=DB_URL,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)


# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     DBSession.remove()


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
