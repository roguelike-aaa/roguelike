import enum
from abc import ABC

from shared.common import Coordinate, Item

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


class CurrentFightStats:
    def __init__(self, current_health, max_health, strength):
        self.current_health = current_health
        self.max_health = max_health
        self.strength = strength


class Player:
    """
        Class storing player position on the map.
    """

    def __init__(self, coordinate: Coordinate, player_token: PlayerToken, fight_stats: CurrentFightStats):
        """
        :param coordinate: position on the map.
        :param player_token: player identifier.
        """
        self.coordinate = coordinate
        self.token = player_token
        self.fight_stats = fight_stats


class Mob:
    def __init__(self, coordinate: Coordinate, mob_mode, fight_stats: CurrentFightStats):
        self.coordinate = coordinate
        self.mob_mode = mob_mode
        self.fight_stats = fight_stats


class PlayerItemState(enum.Enum):
    OFF = enum.auto()
    ACTIVE = enum.auto()


class PlayersItem:
    def __init__(self, item: Item, state=PlayerItemState.OFF):
        self.item = item
        self.state = state


class Inventory:
    def __init__(self, items=None):
        if items is None:
            items = []
        self.active_helmet = None
        self.active_shirt = None
        self.active_weapon = None

        self.items = items


class PlayerMap:
    """
        Class storing a full player knowledge about the game.
    """

    def __init__(self, player_map, player: Player, status_message: str):
        """
        :param player_map: 2-dimensional array of characters describing the map layout visible to player.
        :param player: player class defining hero state on the map.
        """
        self.status_message = status_message
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
    NO = enum.auto()


class ItemActionType(enum.Enum):
    """
        Types of items actions
    """
    DROP = enum.auto()
    USE = enum.auto()
    WEAR = enum.auto()
    REMOVE_FROM_SLOT = enum.auto()


class Change(ABC):
    """
        Abstract class for player change.
    """
    pass


class ItemAction(Change):
    """
        Wrapper for the item action.
    """

    def __init__(self, action_type: ItemActionType, item: Item):
        self.action_type = action_type
        self.item = item


class PlayerMove(Change):
    """
        Wrapper for the move type. (In case if some complex moves will appear).
    """

    def __init__(self, move_type: MoveType):
        self.move_type = move_type


class StateChange:
    """
        Describes the player's state change.
    """

    def __init__(self, change: Change):
        """
        :param change: change that player made.
        """
        self.change = change


# Create new game

class GameSettings:
    """
        Describes new game settings.
    """

    def __init__(self, map_heigh, map_width):
        self.map_height = map_heigh
        self.map_width = map_width
