# -*- coding: utf-8 -*-

import os


def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
