Screenshots
===========

.. image:: https://raw.github.com/vaxXxa/gomoku/master/screenshot.png
    :alt: gomoku
    :align: center

Gomoku game
============

Description
-----------

Implementation `Gomoku`_ realtime game using Websockets.


Description of the game's mechanic
----------------------------------

First of all you must choose your login. Then you can "Join" to the existed games, or "Create" new one.

Dimension - dimension of the board.
Lineup - number of stones, that players must put in a row (horizontal, vertical, diagonally, anti-diagonally).

Also, in any moment players can see general statistics of the games. Just press "Esc" button or click on the blue line on the top of the page.

Have fun :)


Technical description
---------------------

I've used next cool, fresh and awesome stack of technologies:

Backend (game server): Python 3.3, Tornado 3.1, Redis 2.6.14

Backend (stats server): Python 3.3, Django 1.5.1, SQL DB

Frontend: SockJS 0.3.4, jQuery 2.0.3, Less.js 1.4.2, Mustache 0.7.2

Game server communicates with browser by Websocket or Websocket emulation (some fallback protocols if Websocket is not available).
Game server communicates with Stats server by HTTP protocol asynchronously.


Installation
------------

.. code:: bash

    $ git clone git@github.com:vaxXxa/gomoku.git
    $ cd gomoku
    $ mkvirtualenv gomoku --python=python3.3
    $ workon gomoku
    $ pip install -r requirements.txt


Run game server
---------------

.. code:: bash

    $ redis-server /usr/local/etc/redis.conf
    $ python endpoints/game/server.py

Go to http://127.0.0.1:8888/


Run stats server
----------------

.. code:: bash

    $ python endpoints/stats/manage.py syncdb
    $ python endpoints/stats/manage.py runserver

Go to http://127.0.0.1:8000/admin/


.. _`Gomoku`: https://en.wikipedia.org/wiki/Gomoku

### After Credits
By Gomoku games

#Thanks for playing
