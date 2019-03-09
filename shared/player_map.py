import enum

from shared.common import Coordinate


# Player state request

class PlayerMap:
    def __init__(self, player_map, player):
        self.map = player_map
        self.player = player


class Player:
    def __init__(self, coordinate, player_token):
        self.coordinate = coordinate
        self.token = player_token


class PlayerToken:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == self.name

    def __hash__(self):
        return self.name.__hash__()


# Change player state requests

class StateChange:
    def __init__(self, player_move):
        self.player_move = player_move


class PlayerMove:
    def __init__(self, move_type):
        self.move_type = move_type


class MoveType(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()
