# -*- coding: utf-8 -*-

import json
from hashlib import md5
from uuid import uuid4

import tornado.ioloop
import tornado.web
import tornado.autoreload
import tornado.httpclient
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

            yield gen.Task(redis.set, 'player:id:{}'.format(secret), username)
            yield gen.Task(redis.sadd, 'player:all', username)

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
            yield gen.Task(redis.delete, 'player:id:{}'.format(self.secret))
            yield gen.Task(redis.srem, 'player:all', self.username)


class GamesListConnection(BaseConnection):
    @gen.engine
    @expect_json
    def on_message(self, message):
        secret = message.get('secret')

        raw_data = yield gen.Task(redis.get, 'player:id:{}'.format(secret))
        player = None
        if raw_data:
            player = raw_data.decode('utf-8')

        if player:
            games = []
            keys = yield gen.Task(redis.keys, 'game:id:*')
            for key in [i.decode('utf-8') for i in keys]:
                title = yield gen.Task(redis.hget, key, 'title')
                games.append(
                    {
                        'id': int(key.split(':')[2]),
                        'title': title.decode('utf-8')
                    }
                )

            answer = {
                'status': 'ok',
                'games': sorted(games, key=lambda obj: obj.get('id'))
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
    @gen.engine
    @expect_json
    def on_message(self, message):
        secret = message.get('secret')
        errors = []

        raw_data = yield gen.Task(redis.get, 'player:id:{}'.format(secret))
        player = None
        if raw_data:
            player = raw_data.decode('utf-8')

        try:
            dimensions = int(message.get("dimensions"))
            lineup = int(message.get("lineup"))
            color = message.get("color")
        except ValueError:
            errors.append('Wrong config for the game.')

        if not errors and lineup > dimensions:
            errors.append('Lineup must be less than dimensions.')

        if not player:
            errors.append('Problem with secret key.')

        if not errors:
            raw_data = yield gen.Task(redis.incr, 'game:counter')
            game_counter = int(raw_data)

            title = '{0} ({1}x{1}, {2} in row) [{3}]'.format(
                player, dimensions, lineup, color
            )
            data = {
                "creator": player,
                "title": title,
                "dimensions": dimensions,
                "lineup": lineup,
                "color": color
            }
            yield gen.Task(redis.hmset, 'game:id:{}'.format(game_counter), data)

            answer = {
                'status': 'ok'
            }
            self.send(json.dumps(answer))

            games = []
            keys = yield gen.Task(redis.keys, 'game:id:*')
            for key in [i.decode('utf-8') for i in keys]:
                title = yield gen.Task(redis.hget, key, 'title')
                games.append(
                    {
                        'id': int(key.split(':')[2]),
                        'title': title.decode('utf-8')
                    }
                )

            answer = {
                'status': 'ok',
                'games': sorted(games, key=lambda obj: obj.get('id'))
            }
            self.broadcast_all_channel("games_list", json.dumps(answer))
        else:
            self.send_error(errors)


class StatsConnection(BaseConnection):
    @gen.engine
    @expect_json
    def on_message(self, message):
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

    redis = Client()
    redis.connect('localhost')

    http_client = tornado.httpclient.AsyncHTTPClient()

    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop)
    io_loop.start()
