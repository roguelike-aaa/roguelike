import enum


class StateChange:
    def __init__(self, player_move):
        self.player_mode = player_move


class PlayerMove:
    def __init__(self, move_type):
        self.move_type = move_type


class MoveType(enum.Enum):
    LEFT = enum.auto()
