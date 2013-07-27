# -*- coding: utf-8 -*-

import json
from functools import wraps
from tornado import gen


def expect_json(method):
    """Method decorator, which expects JSON like a income message."""
    @wraps(method)
    @gen.coroutine
    def new_method(self, raw_message):
        try:
            message = json.loads(raw_message)
            yield method(self, message)
        except ValueError:
            self.send_error('Bad JSON message.')

    return new_method


def login_required(method):
    """Method decorator, which check is player logged on or not."""
    @wraps(method)
    @gen.coroutine
    def new_method(self, message):
        if self.is_logged:
            yield method(self, message)
        else:
            self.send_error('You must log in.')

    return new_method
