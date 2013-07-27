# -*- coding: utf-8 -*-

import json
from functools import wraps
from clients import redis_client
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


def secret_required(method):
    """Method decorator, which check secret key. If secret key is valid,
    decorator set `self.username` and `self.secret`.
    """
    @wraps(method)
    @gen.coroutine
    def new_method(self, message):
        error = False
        self.secret = message.get('secret')
        if self.secret:
            raw_data = yield gen.Task(
                redis_client.get, 'player:id:{}'.format(self.secret))
            self.username = None
            if raw_data:
                self.username = raw_data.decode('utf-8')
                yield method(self, message)
            else:
                error = True
        else:
            error = True

        if error:
            self.send_error('Your secret key is wrong.')

    return new_method
