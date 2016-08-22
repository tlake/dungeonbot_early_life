# -*- coding: utf-8 -*-

from flask import request, Response
from helpers import eprint


def token_negotiation():
    eprint("in token_negotiation(): request:", request)

    return Response(status=200)
