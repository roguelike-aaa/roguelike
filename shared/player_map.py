import enum

from shared.common import Coordinate

"""
    Classes for interaction between UI and Controller
"""


# Player state request
# UI -> (pulls get map method) -> Controller
# Controller -> (PlayerMap) -> UI

class PlayerToken:
    """
        Token unique for each player.
    """

    def __init__(self, name: str):
        """
        :param name: player username.
        """
        self.name = name

    def __eq__(self, other):
        return self.name == self.name

    def __hash__(self):
        return self.name.__hash__()


class Player:
    """
        Class storing player position on the map.
    """

    def __init__(self, coordinate: Coordinate, player_token: PlayerToken):
        """
        :param coordinate: position on the map.
        :param player_token: player identifier.
        """
        self.coordinate = coordinate
        self.token = player_token


class PlayerMap:
    """
        Class storing a full player knowledge about the game.
    """

    def __init__(self, player_map, player: Player):
        """
        :param player_map: 2-dimensional array of characters describing the map layout visible to player.
        :param player: player class defining hero state on the map.
        """
        self.map = player_map
        self.player = player


# Change player state requests
# UI -> (pulls the state change method) -> Controller -> Ok!

class MoveType(enum.Enum):
    """
        Types of the moves that hero may make.
    """
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()


class PlayerMove:
    """
        Wrapper for the move type. (In case if some complex moves will appear).
    """

    def __init__(self, move_type: MoveType):
        self.move_type = move_type


class StateChange:
    """
        Describes the player's state change.
    """

    def __init__(self, player_move: PlayerMove):
        """
        :param player_move: relative move that player made.
        """
        self.player_move = player_move


# Create new game

class GameSettings:
    """
        Describes new game settings.
    """

    def __init__(self, map_heigh, map_width):
        self.map_height = map_heigh
        self.map_width = map_width
