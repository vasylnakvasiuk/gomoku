# -*- coding: utf-8 -*-

import json
from functools import wraps

from django.http import HttpResponseServerError


def expect_json(view_function):
    """View decorator for simplifying handing of requests that
    expect json.
    """
    @wraps(view_function)
    def new_view_function(request, *args, **kwargs):
        if not request.META.get('CONTENT_TYPE', '').lower().startswith("application/json"):
            return HttpResponseServerError('JSON is expected')

        try:
            post_data = json.loads(request.raw_post_data.decode("utf-8"))
            request.json_post_data = post_data
            return view_function(request, *args, **kwargs)
        except ValueError:
            return HttpResponseServerError('JSON is expected')

    return new_view_function
