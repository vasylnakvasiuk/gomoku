# -*- coding: utf-8 -*-

import json
from hashlib import md5
from uuid import uuid4

import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado import gen

from jinja2 import Environment, FileSystemLoader
from sockjs.tornado import SockJSRouter
from toredis import Client

from multiplex import MultiplexConnection
from connections import BaseConnection
from decorators import expect_json
from utils import rel
import settings


# Index page handler
class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the index page."""
    def get(self):
        env = Environment(loader=FileSystemLoader(settings.TEMPLATE_PATH))
        self.write(env.get_template('index.html').render())


USERS = {}
GAMES = []


# Connections
class UsernameChoiceConnection(BaseConnection):
    username = None

    @gen.engine
    @expect_json
    def on_message(self, message):
        username = message.get('username')

        is_member = yield gen.Task(redis.sismember, "players", username)

        if not is_member:
            secret = md5(str(uuid4()).encode()).hexdigest()

            yield gen.Task(redis.set, secret, username)
            yield gen.Task(redis.sadd, 'players', username)

            self.username = username
            self.secret = secret
            answer = {
                'status': 'ok',
                'username': username,
                'secret': secret
            }
            self.send(json.dumps(answer))
        else:
            self.send_error('Someone already has that username.')

    @gen.engine
    def on_close(self):
        if self.username:
            yield gen.Task(redis.delete, self.secret)
            yield gen.Task(redis.srem, 'players', self.username)


class GamesListConnection(BaseConnection):
    @expect_json
    def on_message(self, message):
        secret = message.get('secret')

        if secret and secret in USERS:
            answer = {
                'status': 'ok',
                'games': [{"id": 1, "title": "asf"}, {"id": 2, "title": "asf"}]
            }
            self.send(json.dumps(answer))
        else:
            self.send_error('Your secret key is wrong.')


class GamesJoinConnection(BaseConnection):
    @expect_json
    def on_message(self, message):
        secret = message.get('secret')

        if secret and secret in USERS:
            answer = {
                'status': 'ok'
            }
            self.send(json.dumps(answer))
        else:
            self.send_error('Can not connect to this game. Try another one.')


class GameCreateConnection(BaseConnection):
    @expect_json
    def on_message(self, message):
        secret = message.get('secret')

        if secret and secret in USERS:
            answer = {
                'status': 'ok'
            }
            self.send(json.dumps(answer))
        else:
            self.send_error('Wrong config for the game.')


class StatsConnection(BaseConnection):
    @expect_json
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

    redis = Client()
    redis.connect('localhost')

    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop)
    io_loop.start()
