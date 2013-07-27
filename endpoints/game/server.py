# -*- coding: utf-8 -*-

import json

import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado import gen

from jinja2 import Environment, FileSystemLoader
from sockjs.tornado import SockJSRouter

from multiplex import MultiplexConnection
from connections import BaseConnection
from decorators import expect_json, login_required
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
    @expect_json
    @gen.coroutine
    def on_message(self, message):
        username = message.get('username')

        is_member = yield gen.Task(redis_client.sismember, "players:all", username)

        if not is_member:
            # Logging in.
            self.create_player(username)

            raw_data = yield gen.Task(redis_client.incr, 'players:counter')
            self.user_id = int(raw_data)

            yield gen.Task(
                redis_client.set,
                'players:id:{}'.format(self.user_id),
                self.username
            )
            yield gen.Task(redis_client.sadd, 'players:all', self.username)

            answer = {
                'status': 'ok',
                'username': self.username,
                'user_id': self.user_id
            }
            self.send(json.dumps(answer))
        else:
            self.send_error('Someone already has that username.')

    @gen.coroutine
    def on_close(self):
        if self.is_logged:
            yield gen.Task(redis_client.delete, 'players:id:{}'.format(self.user_id))
            yield gen.Task(redis_client.srem, 'players:all', self.username)


class GamesListConnection(BaseConnection):
    """Channel connection. Used for managing users."""

    @login_required
    @gen.coroutine
    def on_message(self, message):
        games = yield self.get_games()
        self.send(games)


class GamesJoinConnection(BaseConnection):
    @expect_json
    @login_required
    @gen.coroutine
    def on_message(self, message):
        game_id = message.get('id')

        if True:
            model = {
                'dimensions': 3,
                'cells': [
                    {'x': '2', 'y': '2', 'color': 'white'},
                    {'x': '1', 'y': '1', 'color': 'black'},
                    {'x': '4', 'y': '1', 'color': 'white'}
                ]
            }

            answer = {
                'status': 'ok',
                'model': model
            }
            self.send(json.dumps(answer))
            self.send_channel(
                'note',
                json.dumps({'msg': 'Welcome to the game #{}'.format(game_id)})
            )
            self.get_player('vaxXxa').send_channel(
                'note',
                json.dumps({'msg': 'New user!!!'})
            )
        else:
            self.send_error('Can not connect to this game. Try another one.')


class GameCreateConnection(BaseConnection):
    @expect_json
    @login_required
    @gen.coroutine
    def on_message(self, message):
        errors = []

        try:
            dimensions = int(message.get("dimensions"))
            lineup = int(message.get("lineup"))
            color = message.get("color")
            if not dimensions or not lineup or not color:
                errors.append('Wrong config for the game.')
        except ValueError:
            errors.append('Wrong config for the game.')

        if not errors and lineup > dimensions:
            errors.append('Lineup must be less than dimensions.')

        if not errors:
            raw_data = yield gen.Task(redis_client.incr, 'games:counter')
            game_id = int(raw_data)

            title = '{0} ({1}x{1}, {2} in row) [{3}]'.format(
                self.username, dimensions, lineup, color
            )
            data = {
                "creator": self.username,
                "dimensions": dimensions,
                "lineup": lineup,
                "color": color,
                "cells": []
            }
            yield gen.Task(
                redis_client.hmset, 'games:id:{}'.format(game_id), data)
            yield gen.Task(
                redis_client.sadd, 'games:all',
                '{}:{}'.format(game_id, title))

            game = {
                'game_id': game_id,
                'dimensions': dimensions,
                'cells': []
            }

            self.send(json.dumps({
                'status': 'ok',
                'game': game
            }))

            games = yield self.get_games()
            self.broadcast_all_channel("games_list", games)

            self.send_channel(
                'note',
                json.dumps({'msg': 'Waiting for the opponent...'})
            )
        else:
            self.send_error(errors)


class StatsConnection(BaseConnection):
    @gen.coroutine
    def on_open(self, info):
        url = 'http://localhost:8000/api/player/top'
        response = yield http_client.fetch(url, method="GET")
        self.send(response.body.decode('utf-8'))
        super().on_open(info)


class NoteConnection(BaseConnection):
    pass


class GameActionConnection(BaseConnection):
    @expect_json
    @login_required
    @gen.coroutine
    def on_message(self, message):
        self.send_channel('game_finish', json.dumps(
            {
                'winner': True
            }
        ))


class GameFinishConnection(BaseConnection):
    pass


if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # Create multiplexer
    channels = {
        'username_choice': UsernameChoiceConnection,
        'games_list': GamesListConnection,
        'games_join': GamesJoinConnection,
        'game_create': GameCreateConnection,
        'stats': StatsConnection,
        'note': NoteConnection,
        'game_action': GameActionConnection,
        'game_finish': GameFinishConnection
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
