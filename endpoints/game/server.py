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

from multiplex import MultiplexConnection
from connections import BaseConnection
from decorators import expect_json, secret_required
from utils import rel
from clients import redis_client, http_client
import settings


# Index page handler
class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the index page."""
    def get(self):
        env = Environment(loader=FileSystemLoader(settings.TEMPLATE_PATH))
        self.write(env.get_template('index.html').render())


# Connections
class UsernameChoiceConnection(BaseConnection):
    """Channel connection. Used for managing users."""
    username = None

    @expect_json
    @gen.coroutine
    def on_message(self, message):
        username = message.get('username')

        is_member = yield gen.Task(redis_client.sismember, "player:all", username)

        if not is_member:
            self.username = username
            self.secret = md5(str(uuid4()).encode()).hexdigest()

            yield gen.Task(
                redis_client.set,
                'player:id:{}'.format(self.secret),
                self.username
            )
            yield gen.Task(redis_client.sadd, 'player:all', self.username)

            answer = {
                'status': 'ok',
                'username': self.username,
                'secret': self.secret
            }
            self.send(json.dumps(answer))
        else:
            self.send_error('Someone already has that username.')

    @gen.coroutine
    def on_close(self):
        if self.username:
            yield gen.Task(redis_client.delete, 'player:id:{}'.format(self.secret))
            yield gen.Task(redis_client.srem, 'player:all', self.username)


class GamesListConnection(BaseConnection):
    """Channel connection. Used for managing users."""

    @expect_json
    @secret_required
    @gen.coroutine
    def on_message(self, message):
        games = yield self.get_games()
        self.send(games)


class GamesJoinConnection(BaseConnection):
    @expect_json
    @secret_required
    @gen.coroutine
    def on_message(self, message):
        if self.secret and self.secret in []:
            answer = {
                'status': 'ok'
            }
            self.send(json.dumps(answer))
        else:
            self.send_error('Can not connect to this game. Try another one.')


class GameCreateConnection(BaseConnection):
    @expect_json
    @secret_required
    @gen.coroutine
    def on_message(self, message):
        errors = []

        try:
            dimensions = int(message.get("dimensions"))
            lineup = int(message.get("lineup"))
            color = message.get("color")
        except ValueError:
            errors.append('Wrong config for the game.')

        if not errors and lineup > dimensions:
            errors.append('Lineup must be less than dimensions.')

        if not errors:
            raw_data = yield gen.Task(redis_client.incr, 'game:counter')
            game_counter = int(raw_data)

            title = '{0} ({1}x{1}, {2} in row) [{3}]'.format(
                self.username, dimensions, lineup, color
            )
            data = {
                "creator": self.username,
                "title": title,
                "dimensions": dimensions,
                "lineup": lineup,
                "color": color
            }
            yield gen.Task(redis_client.hmset, 'game:id:{}'.format(game_counter), data)

            answer = {
                'status': 'ok'
            }
            self.send(json.dumps(answer))

            games = yield self.get_games()
            self.broadcast_all_channel("games_list", games)
        else:
            self.send_error(errors)


class StatsConnection(BaseConnection):
    @gen.coroutine
    def on_open(self, info):
        url = 'http://localhost:8000/api/player/top'
        response = yield http_client.fetch(url, method="GET")
        self.send(response.body.decode('utf-8'))


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
