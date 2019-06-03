"""
    Classes for interaction between map generator and controller.
"""

# Map request
# Controller -> (MapConfig) -> MapGenerator
# MapGenerator -> (GeneratedMap) -> Controller
import enum

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

    def __init__(self, game_map, player_init_states, mobs, clothes):
        """
        :param game_map: 2-dimensional array of CellType elements of height x width size.
        :param player_init_states: player state at the beginning of the game.
        """
        self.map = game_map
        self.player_init_states = player_init_states
        self.mobs = mobs
        self.clothes = clothes


class PlayerInitState:
    """
        State of the player at the beginning og the game.
    """

    def __init__(self, coordinate, fight_stats):
        """
        :param coordinate: player starting coordinate.
        """
        self.fight_stats = fight_stats
        self.coordinate = coordinate


class ModMode(enum.Enum):
    FRIGHTENED = enum.auto()
    AGGRESSIVE = enum.auto()
    PASSIVE = enum.auto()


class MobInitState:
    """
        State of the mob at the beginning og the game.
    """

    def __init__(self, coordinate, fight_stats, mob_mode):
        """
        :param coordinate: mob starting coordinate.
        """
        self.fight_stats = fight_stats
        self.coordinate = coordinate
        self.mob_mode = mob_mode


class ClothesInitState:
    """
        State of the clothes and stuff at the beginning of the game.
    """

    def __init__(self, coordinate, clothes_stats):
        self.coordinate = coordinate
        self.clothes_stats = clothes_stats


class FightStats:
    def __init__(self, health, strength):
        """
        :param health: unit init max health
        :param strength: unit init strength
        """
        self.health = health
        self.strength = strength


class ClothesStats:
    def __init__(self, health_add, strength_add):
        """
        :param health_add: what will be added to character's health
        :param strength: what will be added to character's strength
        """
        self.health_add = health_add
        self.strength_add = strength_add


class ItemState:
    def __init__(self, coordinate: Coordinate, item: Item):
        self.coordinate = coordinate
        self.item = item
