# -*- coding: utf-8 -*-

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


# Connections
class UsernameConnection(ChannelConnection, MultiParticipantsConnection):
    def on_message(self, message):
        if message == 'vaxxxa':
            answer = {'status': 'ok'}
        else:
            answer = {'status': 'error', 'errormsg': 'AAA!!!'}
        self.send(answer)


class GameListConnection(ChannelConnection, MultiParticipantsConnection):
    def on_message(self, message):
        self.broadcast_all_channel('username', 'Hello world!')


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
