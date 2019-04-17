"""
    Classes for interaction between map generator and controller.
"""

# Map request
# Controller -> (MapConfig) -> MapGenerator
# MapGenerator -> (GeneratedMap) -> Controller
import enum


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

    def __init__(self, game_map, player_init_states, mobs):
        """
        :param game_map: 2-dimensional array of CellType elements of height x width size.
        :param player_init_states: player state at the beginning of the game.
        """
        self.map = game_map
        self.player_init_states = player_init_states
        self.mobs = mobs


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


class FightStats:
    def __init__(self, health, strength):
        """
        :param health: unit init max health
        :param strength: unit init strength
        """
        self.health = health
        self.strength = strength
