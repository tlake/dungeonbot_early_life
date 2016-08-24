# -*- coding: utf-8 -*-

"""
A tiny Flask app to verify the URL for Slack's Events API.
"""

from flask import Flask, render_template, request, Response
from oauth import token_negotiation
from command import parse_command
import os

from auxiliaries.helpers import eprint


################################
# APP SETTINGS
################################

app = Flask(__name__)
app.debug = True


if app.debug:
    import logging
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    app.logger.addHandler(stream_handler)


################################
# TOOLS
################################

def event_is_important(evt):
    if (evt['user'] != os.getenv("BOT_ID")) and (evt['text'][0] == "!"):
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

    if event_is_important(event):
        event['text'] = event['text'][1:]  # strip out the '!' command prefix
        parse_command(event)

    return Response(status=200)


@app.route("/oauth", methods=["GET", "POST"])
def oauth():
    eprint("hit /oauth route")

    return token_negotiation()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
