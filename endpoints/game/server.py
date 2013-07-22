# -*- coding: utf-8 -*-

import json
from hashlib import md5
from uuid import uuid4

import tornado.ioloop
import tornado.web
import tornado.autoreload

from sockjs.tornado import SockJSRouter
from multiplex import MultiplexConnection

from connections import MultiParticipantsConnection, ChannelConnection

from utils import rel


# Index page handler
class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render('templates/base.html')


USERS = {}
GAMES = []


# Connections
class UsernameConnection(ChannelConnection, MultiParticipantsConnection):
    def on_message(self, message):
        data = json.loads(message)
        username = data.get('username')

        if username and username not in USERS.values():
            secret_key = md5(str(uuid4()).encode()).hexdigest()
            USERS.update({secret_key: username})
            answer = {
                'status': 'ok',
                'username': username,
                'secret': secret_key
            }
        else:
            answer = {
                'status': 'error',
                'errormsg': 'Someone already has that username.'
            }
        self.send(json.dumps(answer))


class GameListConnection(ChannelConnection, MultiParticipantsConnection):
    def on_message(self, message):
        data = json.loads(message)

        if data.get('action') == 'get_list':
            self.send(json.dumps({
                'games': GAMES
            }))
        elif data.get('action') == 'create_game':
            GAMES.append({
                'username': USERS.get(data['secret']),
            })
            self.broadcast_all(json.dumps({
                'games': GAMES
            }))


if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # Create multiplexer
    router = MultiplexConnection.get(
        username=UsernameConnection,
        gamelist=GameListConnection)

    # Register multiplexer
    MainSocketRouter = SockJSRouter(router, '/socket')

    # Create application
    app = tornado.web.Application(
        [
            (r'/', IndexHandler),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': rel('static')},),
        ] + MainSocketRouter.urls
    )
    app.listen(8888)
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop)
    io_loop.start()
