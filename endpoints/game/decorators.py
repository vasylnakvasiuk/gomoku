# -*- coding: utf-8 -*-

import json
from functools import wraps


def expect_json(method):
    """Method decorator, which expects JSON like a income message."""
    @wraps(method)
    def new_method(self, raw_message):
        try:
            message = json.loads(raw_message)
            return method(self, message)
        except ValueError:
            self.send_error('Bad JSON message.')

    return new_method
