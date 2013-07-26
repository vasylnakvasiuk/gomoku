# -*- coding: utf-8 -*-


class ErrorException(Exception):
    """ErrorException for error response."""

    @property
    def response(self):
        msg = self.args[0]
        if isinstance(msg, list):
            errors = msg
        else:
            errors = [msg]
        return {
            'status': 'error',
            'errors': errors
        }
