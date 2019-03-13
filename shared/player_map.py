import enum

from shared.common import Coordinate


# Player state request

class PlayerToken:
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return self.name == self.name

    def __hash__(self):
        return self.name.__hash__()


class Player:
    def __init__(self, coordinate: Coordinate, player_token: PlayerToken):
        self.coordinate = coordinate
        self.token = player_token


class PlayerMap:
    def __init__(self, player_map, player: Player):
        self.map = player_map
        self.player = player


# Change player state requests


class MoveType(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()


class PlayerMove:
    def __init__(self, move_type: MoveType):
        self.move_type = move_type


class StateChange:
    def __init__(self, player_move: PlayerMove):
        self.player_move = player_move
