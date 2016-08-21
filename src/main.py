# import os
# from slacker import Slacker


# if __name__ == "__main__":
#     pass


# -*- coding: utf-8 -*-

"""
A tiny Flask app to verify the URL for Slack's Events API.
"""

from flask import Flask, Response, request
from helpers import eprint


################################
# APP SETTINGS
################################

app = Flask(__name__)


################################
# API ROUTES
################################

@app.route("/", methods=["GET"])
def verify():
    eprint(dir(request))

    return Response(
        status=200,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
