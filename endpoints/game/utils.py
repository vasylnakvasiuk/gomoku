# -*- coding: utf-8 -*-

import os


def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)


def hgetall_group_by(lst):
    """List of data from redis hash to dict."""
    lst = [i.decode('utf-8') for i in lst]
    return dict(zip(*[lst[i::2] for i in range(2)]))
