# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
import tornado.autoreload
import tornado.options

from jinja2 import Environment, FileSystemLoader
from sockjs.tornado import SockJSRouter

from multiplex import MultiplexConnection
import connections
from utils import rel
import settings


class IndexHandler(tornado.web.RequestHandler):
    """Regular HTTP handler to serve the index page."""
    def get(self):
        env = Environment(loader=FileSystemLoader(settings.TEMPLATE_PATH))
        self.write(env.get_template('index.html').render())

if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)
    tornado.options.define("port", default=8888, help="Run on port", type=int)
    tornado.options.define("address", default='localhost', help="Run on host", type=str)
    tornado.options.parse_command_line()

    # Create multiplexer
    channels = {
        'username_choice': connections.UsernameChoiceConnection,
        'stats': connections.StatsConnection,
        'note': connections.NoteConnection,
        'games_list': connections.GamesListConnection,
        'games_join': connections.GamesJoinConnection,
        'game_create': connections.GameCreateConnection,
        'game_action': connections.GameActionConnection,
        'game_finish': connections.GameFinishConnection
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
    app.listen(
        tornado.options.options.port,
        address=tornado.options.options.address
    )

    io_loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(io_loop)
    io_loop.start()
