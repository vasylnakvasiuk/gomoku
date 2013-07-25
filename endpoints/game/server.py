# -*- coding: utf-8 -*-

import json
from hashlib import md5
from uuid import uuid4

import tornado.ioloop
import tornado.web
import tornado.autoreload

from jinja2 import Environment, FileSystemLoader
from sockjs.tornado import SockJSRouter

from multiplex import MultiplexConnection
from connections import MultiParticipantsConnection, ChannelConnection
from utils import rel
import settings


# Index page handler
class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        env = Environment(loader=FileSystemLoader(settings.TEMPLATE_PATH))
        self.write(env.get_template('index.html').render())


USERS = {}
GAMES = []


# Connections
class UsernameChoiceConnection(ChannelConnection, MultiParticipantsConnection):
    def on_message(self, message):
        data = json.loads(message)
        username = data.get('username')

        if username and username not in USERS.values():
            secret = md5(str(uuid4()).encode()).hexdigest()
            USERS.update({secret: username})
            answer = {
                'status': 'ok',
                'username': username,
                'secret': secret
            }
        else:
            answer = {
                'status': 'error',
                'errors': ['Someone already has that username.']
            }
        self.send(json.dumps(answer))


class GamesListConnection(ChannelConnection, MultiParticipantsConnection):
    def on_message(self, message):
        data = json.loads(message)
        secret = data.get('secret')

        if secret and secret in USERS:
            answer = {
                'status': 'ok',
                'games': [{"id": 1, "title": "asf"}, {"id": 2, "title": "asf"}]
            }
        else:
            answer = {
                'status': 'error',
                'errors': ['Your secret key is wrong.']
            }
        self.send(json.dumps(answer))


class GamesJoinConnection(ChannelConnection, MultiParticipantsConnection):
    def on_message(self, message):
        data = json.loads(message)
        secret = data.get('secret')

        if secret and secret in USERS:
            answer = {
                'status': 'ok'
            }
        else:
            answer = {
                'status': 'error',
                'errors': ['Can not connect to this game. Try another one.']
            }
        self.send(json.dumps(answer))


class GameCreateConnection(ChannelConnection, MultiParticipantsConnection):
    def on_message(self, message):
        data = json.loads(message)
        secret = data.get('secret')

        if secret and secret in USERS:
            answer = {
                'status': 'ok'
            }
        else:
            answer = {
                'status': 'error',
                'errors': ['Wrong config for the game.']
            }
        self.send(json.dumps(answer))


class StatsConnection(ChannelConnection, MultiParticipantsConnection):
    def on_message(self, message):
        answer = [
            {
                'name': 'Vasia',
                'quantity': 10,
                'wins': 5,
                'losses': 2,
                'draws': 3
            },
            {
                'name': 'Igor',
                'quantity': 1,
                'wins': 1,
                'losses': 0,
                'draws': 0
            },
            {
                'name': 'Rob',
                'quantity': 6,
                'wins': 1,
                'losses': 2,
                'draws': 3
            }
        ]
        self.send(json.dumps(answer))


if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # Create multiplexer
    channels = {
        "username_choice": UsernameChoiceConnection,
        "games_list": GamesListConnection,
        "games_join": GamesJoinConnection,
        "game_create": GameCreateConnection,
        "stats": StatsConnection
    }

    router = MultiplexConnection.get(**channels)

    # Register multiplexer
    MainSocketRouter = SockJSRouter(router, '/socket')

    # Create application
    app = tornado.web.Application(
        [
            (r'/', IndexHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': rel('static')},),
        ] + MainSocketRouter.urls
    )
    app.listen(settings.PORT)

    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop)
    io_loop.start()
