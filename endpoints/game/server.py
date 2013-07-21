# -*- coding: utf-8 -*-

import json

import tornado.ioloop
import tornado.web
import tornado.autoreload

from sockjs.tornado import SockJSConnection, SockJSRouter
from multiplex import MultiplexConnection


# Index page handler
class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the chatroom page"""
    def get(self):
        self.render('templates/base.html')


# Connections
class UsernameConnection(SockJSConnection):
    def on_open(self, info):
        # self.send('Username says hi!!')
        pass

    def on_message(self, message):
        if message == 'vaxxxa':
            answer = {'status': 'ok'}
        else:
            answer = {'status': 'error', 'errormsg': 'AAA!!!'}
        self.send(json.dumps(answer))


class GameListConnection(SockJSConnection):
    def on_open(self, info):
        self.send('Game list says hi!!')

    def on_message(self, message):
        self.send('Game list nods: ' + message)


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
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': './static'},),
        ] + MainSocketRouter.urls
    )
    app.listen(8888)
    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop)
    io_loop.start()
