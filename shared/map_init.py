"""
    Classes for interaction between map generator and controller.
"""

# Map request
# Controller -> (MapConfig) -> MapGenerator
# MapGenerator -> (GeneratedMap) -> Controller
import enum
from abc import ABC

from shared.common import Coordinate, Bonus, Item


class MapConfig:
    """
        Map meta information.
    """

    def __init__(self, height, width):
        """
        :param width: map width
        :param height: map height
        """
        self.width = width
        self.height = height


class GeneratedMap:
    """
        Class storing the map layout and players states on the map.
    """

    def __init__(self, game_map, player_init_states, mobs, items):
        """
        :param game_map: 2-dimensional array of CellType elements of height x width size.
        :param player_init_states: player state at the beginning of the game.
        """
        self.map = game_map
        self.player_init_states = player_init_states
        self.mobs = mobs
        self.items = items


class FightStats:
    def __init__(self, health, strength):
        """
        :param health: unit init max health
        :param strength: unit init strength
        """
        self.health = health
        self.strength = strength


class MapObjectInitState(ABC):
    def __init__(self, coordinate: Coordinate):
        self.coordinate = coordinate


class UnitInitState(MapObjectInitState):
    def __init__(self, coordinate: Coordinate, fight_stats: FightStats):
        super().__init__(coordinate)
        self.fight_stats = fight_stats


class PlayerInitState(UnitInitState):
    """
        State of the player at the beginning og the game.
    """

    def __init__(self, coordinate: Coordinate, fight_stats: FightStats):
        """
        :param coordinate: player starting coordinate.
        """
        super().__init__(coordinate, fight_stats)


class ModMode(enum.Enum):
    FRIGHTENED = enum.auto()
    AGGRESSIVE = enum.auto()
    PASSIVE = enum.auto()


class MobInitState(UnitInitState):
    """
        State of the mob at the beginning og the game.
    """

    def __init__(self, coordinate, fight_stats, mob_mode):
        """
        :param coordinate: mob starting coordinate.
        """
        super().__init__(coordinate, fight_stats)
        self.mob_mode = mob_mode


class ItemInitState(MapObjectInitState):
    def __init__(self, coordinate: Coordinate, item: Item):
        super().__init__(coordinate)
        self.item = item
