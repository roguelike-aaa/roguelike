"""
    Classes for interaction between map generator and controller.
"""


# Map request
# Controller -> (MapConfig) -> MapGenerator
# MapGenerator -> (GeneratedMap) -> Controller

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
    def __init__(self, game_map, players_init_state):
        """
        :param game_map: 2-dimensional array of CellType elements of height x width size.
        :param players_init_state: player state at the beginning of the game.
        """
        self.map = game_map
        self.player_init_states = players_init_state


class PlayerInitState:
    """
        State of the player at the beginning og the game.
    """
    def __init__(self, coordinate):
        """
        :param coordinate: player starting coordinate.
        """
        self.coordinate = coordinate
