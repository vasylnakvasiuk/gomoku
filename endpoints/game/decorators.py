# -*- coding: utf-8 -*-

import json
from functools import wraps

from exceptions import ErrorException


def expect_json(method):
    """Method decorator, which expects JSON like a income message."""
    @wraps(method)
    def new_method(self, raw_message):
        try:
            message = json.loads(raw_message)
            return method(self, message)
        except ValueError:
            raise ErrorException('Bad JSON message.')

    return new_method


def catch_exceptions(method):
    """Method decorator for `sockjs.tornado.session`, which catches
    `ErrorException` and send message about errors.
    """
    @wraps(method)
    def new_method(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except ErrorException as e:
            self.send_message(json.dumps(e.response))
            return

    return new_method
