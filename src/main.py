# -*- coding: utf-8 -*-

"""
A tiny Flask app to verify the URL for Slack's Events API.
"""

from flask import Flask, render_template, request, Response
from oauth import token_negotiation
from slacker import Slacker
import os


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

def we_care(evt):
    if (evt['user'] != os.getenv("BOT_ID")) and (evt['text'][0] == "!"):
        return True
    return False


################################
# API ROUTES
################################

@app.route("/", methods=["GET", "POST"])
def root():
    from helpers import eprint
    eprint("hit / route")

    if request.method == "GET":
        return render_template("index.html")

    BOT = Slacker(os.getenv("BOT_ACCESS_TOKEN"))

    if we_care(request.json['event']):
        BOT.chat.post_message(
            request.json['event']['channel'],
            request.json['event']['text'],
            as_user=True,
        )

    return Response(status=200)


@app.route("/oauth", methods=["GET", "POST"])
def oauth():
    from helpers import eprint
    eprint("hit /oauth route")

    return token_negotiation()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
