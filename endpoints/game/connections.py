# -*- coding: utf-8 -*-

import json

from tornado import gen
from sockjs.tornado import SockJSConnection

from clients import redis_client


class MultiParticipantsConnection(SockJSConnection):
    """Connection, which save participants and support additional
    methods for working with participants.
    """
    participants = set()

    def on_open(self, info):
        self.participants.add(self)
        super().on_open(info)

    def broadcast_all(self, message):
        """Broadcast message to all participants."""
        target_class = self.__class__
        targets = [i for i in self.participants if isinstance(i, target_class)]
        self.broadcast(targets, message)

    def on_close(self):
        self.participants.remove(self)
        super().on_close()


class ChannelConnection(SockJSConnection):
    """Connection, for working with multiplex channels."""
    def send_channel(self, channel, message, binary=False):
        """Send message to the specific channel."""
        if not self.is_closed:
            self.session.send_message_channel(channel, message, binary=binary)

    def broadcast_channel(self, channel, clients, message):
        """Broadcast message to some participants for the specific
        channel.
        """
        self.session.broadcast_channel(channel, clients, message)

    def broadcast_all_channel(self, channel, message):
        """Broadcast message to all participants for the specific
        channel. This method expects, that `participants` property is
        already exists (using, for example, `MultiParticipantsConnection`).
        """
        target_class = self.__class__
        targets = [i for i in self.participants if isinstance(i, target_class)]
        self.session.broadcast_channel(channel, targets, message)


class ErrorConnection(SockJSConnection):
    """Connection, for working with multiplex channels."""
    def send_error(self, message):
        if isinstance(message, list):
            errors = message
        else:
            errors = [message]

        self.send(json.dumps(
            {
                'status': 'error',
                'errors': errors
            }
        ))


class BaseConnection(ChannelConnection, MultiParticipantsConnection, ErrorConnection):
    """Base connection for working with sockets."""

    players = {}

    def on_close(self):
        self.remove_player()
        super().on_close()

    def create_player(self, username):
        """Create player for current connection."""
        self.username = username
        self.players[username] = self

    def remove_player(self):
        """Remove player for current connection."""
        if self.is_logged:
            del self.players[self.username]
            self.username = None

    def get_player(self, username):
        """Get player by username from all connections."""
        return self.players.get(username)

    @property
    def is_logged(self):
        """Check player login status for current connection."""
        return bool(self.username)

    @property
    def username(self):
        if hasattr(self.session, 'base'):
            return getattr(self.session.base, 'username', None)
        return None

    @username.setter
    def username(self, value):
        if hasattr(self.session, 'base'):
            setattr(self.session.base, 'username', value)

    @gen.coroutine
    def get_games(self):
        """Return serialized list of games."""
        games = []
        keys = yield gen.Task(redis_client.keys, 'game:id:*')
        # TODO: improve these multi queries.
        for key in [i.decode('utf-8') for i in keys]:
            title = yield gen.Task(redis_client.hget, key, 'title')
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
        # TODO: is it ok to use return?
        return json.dumps(answer)
