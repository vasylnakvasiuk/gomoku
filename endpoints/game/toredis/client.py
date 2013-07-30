import logging
import socket

from collections import deque

import hiredis

from tornado.iostream import IOStream
from tornado.ioloop import IOLoop
from tornado import stack_context

from toredis.commands import RedisCommandsMixin


logger = logging.getLogger(__name__)


class Client(RedisCommandsMixin):
    """
        Redis client class
    """
    def __init__(self, io_loop=None):
        """
            Constructor

            :param io_loop:
                Optional IOLoop instance
        """
        self._io_loop = io_loop or IOLoop.instance()

        self._stream = None

        self.reader = None
        self.callbacks = deque()

        self._sub_callback = False

    def connect(self, host='localhost', port=6379, callback=None):
        """
            Connect to redis server

            :param host:
                Host to connect to
            :param port:
                Port
            :param callback:
                Optional callback to be triggered upon connection
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        return self._connect(sock, (host, port), callback)

    def connect_usocket(self, usock, callback=None):
        """
            Connect to redis server with unix socket
        """
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        return self._connect(sock, usock, callback)

    def on_disconnect(self):
        """
            Override this method if you want to handle disconnections
        """
        pass

    # State
    def is_idle(self):
        """
            Check if client is not waiting for any responses
        """
        return len(self.callbacks) == 0

    def is_connected(self):
        """
            Check if client is still connected
        """
        return bool(self._stream) and not self._stream.closed()

    def send_message(self, args, callback=None):
        """
            Send command to redis

            :param args:
                Arguments to send
            :param callback:
                Callback
        """
        # Special case for pub-sub
        cmd = args[0]

        if (self._sub_callback is not None and
            cmd not in ('PSUBSCRIBE', 'SUBSCRIBE', 'PUNSUBSCRIBE', 'UNSUBSCRIBE')):
            raise ValueError('Cannot run normal command over PUBSUB connection')

        # Send command
        self._stream.write(self.format_message(args))
        if callback is not None:
            callback = stack_context.wrap(callback)
        self.callbacks.append(callback)

    def format_message(self, args):
        """
            Create redis message

            :param args:
                Message data
        """
        l = "*%d" % len(args)
        lines = [l.encode('utf-8')]
        for arg in args:
            if not isinstance(arg, str):
                arg = str(arg)
            arg = arg.encode('utf-8')
            l = "$%d" % len(arg)
            lines.append(l.encode('utf-8'))
            lines.append(arg)
        lines.append(b"")
        return b"\r\n".join(lines)

    def close(self):
        """
            Close redis connection
        """
        self.quit()
        self._stream.close()

    # Pub/sub commands
    def psubscribe(self, patterns, callback=None):
        """
            Customized psubscribe command - will keep one callback for all incoming messages

            :param patterns:
                string or list of strings
            :param callback:
                callback
        """
        self._set_sub_callback(callback)
        super(Client, self).psubscribe(patterns)

    def subscribe(self, channels, callback=None):
        """
            Customized subscribe command - will keep one callback for all incoming messages

            :param channels:
                string or list of strings
            :param callback:
                Callback
        """
        self._set_sub_callback(callback)
        super(Client, self).subscribe(channels)

    def _set_sub_callback(self, callback):
        if self._sub_callback is None:
            self._sub_callback = callback

        assert self._sub_callback == callback

    # Helpers
    def _connect(self, sock, addr, callback):
        self._reset()

        self._stream = IOStream(sock, io_loop=self._io_loop)
        self._stream.connect(addr, callback=callback)
        self._stream.read_until_close(self._on_close, self._on_read)

    # Event handlers
    def _on_read(self, data):
        self.reader.feed(data)

        resp = self.reader.gets()

        while resp is not False:
            if self._sub_callback:
                try:
                    self._sub_callback(resp)
                except:
                    logger.exception('SUB callback failed')
            else:
                if self.callbacks:
                    callback = self.callbacks.popleft()
                    if callback is not None:
                        try:
                            callback(resp)
                        except:
                            logger.exception('Callback failed')
                else:
                    logger.debug('Ignored response: %s' % repr(resp))

            resp = self.reader.gets()

    def _on_close(self, data=None):
        if data is not None:
            self._on_read(data)

        # Trigger any pending callbacks
        callbacks = self.callbacks
        self.callbacks = deque()

        if callbacks:
            for cb in callbacks:
                if cb is not None:
                    try:
                        cb(None)
                    except:
                        logger.exception('Exception in callback')

        if self._sub_callback is not None:
            try:
                self._sub_callback(None)
            except:
                logger.exception('Exception in SUB callback')
            self._sub_callback = None

        # Trigger on_disconnect
        self.on_disconnect()

    def _reset(self):
        self.reader = hiredis.Reader()
        self._sub_callback = None
