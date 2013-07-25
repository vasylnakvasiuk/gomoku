Gomoku game
============

Description
-----------

Implementation `Gomoku`_ realtime game using Websockets.


Technologies
------------

Backend (game server): Python 3.3, Tornado 3.1, sockjs-tornado 1.0.0, Jinja2 2.7

Backend (stats server): Python 3.3, Django 1.5.1, redis 2.7.6

Frontend: SockJS 0.3.4, jQuery 2.0.3, Less.js 1.4.2, Mustache 0.7.2, Websocket-Multiplexer 0.1


Installation
------------

Some description.

.. code:: bash

    $ git clone git@github.com:vaxXxa/gomoku.git
    $ cd gomoku
    $ python server.py
    $ redis-server /usr/local/etc/redis.conf


.. _`Gomoku`: https://en.wikipedia.org/wiki/Gomoku