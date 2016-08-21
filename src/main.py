# -*- coding: utf-8 -*-

"""
A tiny Flask app to verify the URL for Slack's Events API.
"""

from flask import Flask, render_template, Response
from helpers import eprint


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
# API ROUTES
################################

@app.route("/", methods=["GET"])
def root():
    eprint("hit / route")
    return render_template("index.html")


@app.route("/oauth", methods=["GET", "POST"])
def oauth():
    eprint("hit /oauth route")
    return Response(status=200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
