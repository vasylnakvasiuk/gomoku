# -*- coding: utf-8 -*-

import json
import re
from tornado import gen

from base_connections import BaseConnection
from decorators import expect_json, login_required
from clients import redis_client, http_client
from utils import hgetall_group_by
from play import Game

reg = re.compile(r'^[a-zA-Z0-9_.-]+$')


class UsernameChoiceConnection(BaseConnection):
    """Channel connection. Used for managing users."""
    @expect_json
    @gen.coroutine
    def on_message(self, message):
        username = message.get('username')

        is_member = yield gen.Task(
            redis_client.sismember, "players:all", username)

        if reg.match(username) and not is_member:
            # Logging in.
            yield self.create_player(username)

            answer = {
                'status': 'ok',
                'username': self.username,
                'user_id': self.user_id
            }
            self.send(json.dumps(answer))
        else:
            self.send_error('Bad username or someone already has this one.')


class StatsConnection(BaseConnection):
    @gen.coroutine
    def on_open(self, info):
        url = 'http://localhost:8000/api/player/top'
        response = yield http_client.fetch(url, method="GET")
        self.send(response.body.decode('utf-8'))
        super().on_open(info)


class NoteConnection(BaseConnection):
    pass


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
        errors = []
        game_id = message.get('game_id')

        raw_data = yield gen.Task(
            redis_client.hmget, 'games:id:{}'.format(game_id),
            ['dimensions', 'matrix', 'creator', 'opponent', 'color', 'lineup']
        )

        if raw_data[0] is None:
            errors.append('Wrong game id.')

        if not errors:
            dimensions = int(raw_data[0])
            matrix = json.loads(raw_data[1].decode('utf-8'))
            creator = raw_data[2].decode('utf-8')
            opponent = raw_data[3] and raw_data[3].decode('utf-8')
            color = raw_data[4].decode('utf-8')
            lineup = raw_data[5].decode('utf-8')

            if opponent is not None:
                errors.append('Game is already started.')

            if self.username == creator:
                errors.append("You can't play with youself.")

        if not errors:
            opponent = self.username
            data_to_save = {'opponent': opponent}

            game = {
                'game_id': game_id,
                'dimensions': dimensions,
                'cells': Game(matrix, dimensions).serialize_cells()
            }

            self.send(json.dumps({
                'status': 'ok',
                'game': game
            }))

            if color == 'black':
                data_to_save.update({'turn': creator})
                opponent_msg = 'You stone is white.'
                creator_msg = 'You stone is black, and now your turn.'
            else:
                data_to_save.update({'turn': opponent})
                creator_msg = 'You stone is white.'
                opponent_msg = 'You stone is black, and now your turn.'

            yield gen.Task(
                redis_client.hmset, 'games:id:{}'.format(game_id),
                data_to_save)

            title = '{0} ({1}x{1}, {2} in row) [{3}]'.format(
                creator, dimensions, lineup, color)
            yield gen.Task(
                redis_client.srem, 'games:all',
                '{}:{}'.format(game_id, title))
            games = yield self.get_games()
            self.broadcast_all_channel("games_list", games)

            self.send_channel(
                'note',
                json.dumps({'msg': 'Welcome to the game #{}. {}'.format(
                    game_id, opponent_msg)}))
            self.get_player(creator).send_channel(
                'note',
                json.dumps({'msg': 'Joining new user "{}". {}'.format(
                    opponent, creator_msg)}))
        else:
            self.send_error(errors)


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

        if not errors and not (3 <= dimensions <= 30):
            errors.append('Dimensions must be from 3 to 30.')

        if not errors and not (3 <= lineup <= 30):
            errors.append('Lineup must be from 3 to 30.')

        if not errors and color not in ['black', 'white']:
            errors.append('Color must be "black" or "white".')

        if not errors and lineup > dimensions:
            errors.append('Lineup must be less than dimensions.')

        if not errors:
            raw_data = yield gen.Task(redis_client.incr, 'games:counter')
            game_id = int(raw_data)

            title = '{0} ({1}x{1}, {2} in row) [{3}]'.format(
                self.username, dimensions, lineup, color
            )
            data = {
                'creator': self.username,
                'dimensions': dimensions,
                'lineup': lineup,
                'color': color,
                'matrix': []
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


class GameActionConnection(BaseConnection):
    @expect_json
    @login_required
    @gen.coroutine
    def on_message(self, message):
        errors = []
        game_id = message.get('game_id')

        raw_data = yield gen.Task(
            redis_client.hgetall, 'games:id:{}'.format(game_id)
        )
        if not raw_data:
            errors.append('This game not existed or already finished.')

        if not errors:
            data = hgetall_group_by(raw_data)

        if not errors and 'opponent' not in data:
            errors.append('Need opponent to join to the game.')

        if not errors:
            creator = data['creator']
            opponent = data['opponent']
            dimensions = int(data['dimensions'])
            lineup = int(data['lineup'])
            color = data['color']
            turn = data['turn']
            matrix = json.loads(data['matrix'])

        if not errors and self.username not in [creator, opponent]:
            errors.append("You are not participant of this game.")

        if not errors and self.username != turn:
            errors.append(
                "It's not your turn. Please, wait for your opponent's move.")

        if not errors:
            game = Game(matrix, dimensions, lineup)

            if self.username == creator:
                action_color = color
            else:
                action_color = 'white' if color == 'black' else 'black'

            color_dict = {
                'white': 0,
                'black': 1
            }
            action = game.action(
                message['x'], message['y'], color_dict[action_color])
            if not action:
                errors.append('Bad action.')

        if not errors:
            turn = opponent if turn == creator else creator
            yield gen.Task(
                redis_client.hset, 'games:id:{}'.format(game_id),
                'turn', turn)
            yield gen.Task(
                redis_client.hset, 'games:id:{}'.format(game_id),
                'matrix', json.dumps(game.matrix))

        if not errors:
            for username in [opponent, creator]:
                player = self.get_player(username)
                player.send_channel(
                    'game_action',
                    json.dumps({
                        'status': 'ok',
                        'action': {
                            'x': message['x'],
                            'y': message['y'],
                            'color': action_color
                        }
                    })
                )

                if turn == username:
                    msg = "Now it's your turn."
                else:
                    msg = "Now it's a {}'s turn. Waiting...".format(
                        opponent if username == creator else creator)
                player.send_channel('note', json.dumps({'msg': msg}))
        else:
            self.send_error(errors)

        if game.is_finished():
            for username in [opponent, creator]:
                player = self.get_player(username)
                player.send_channel(
                    'game_finish', json.dumps({'winner': None})
                )


class GameFinishConnection(BaseConnection):
    pass
