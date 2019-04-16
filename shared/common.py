import enum

"""
    General game elements shared between all components.
"""


class Map:
    """
        Class storing map layout. Includes only elements listed in the CellType enum below.
    """

    def __init__(self, height: int, width: int, map_array):
        """
        :param height: height of the map.
        :param width: width of the map.
        :param map_array: list of height lists each containing exactly width CellType items.
        """

        self.width = width
        self.height = height
        self.map_array = map_array

    def get_cell(self, height: int, width: int):
        """
        Cell content getter.

        :param height: height coordinate of the required cell.
        :param width: width coordinate of the required cell.
        :return: content of the cell if it existed. Otherwise returns CellType.ERROR value.
        """
        return self.map_array[height][
            width] if 0 <= height < self.height and 0 <= width < self.width else CellType.ERROR


class Coordinate:
    """
        Class storing a position on the map.
    """

    def __init__(self, x: int, y: int):
        """
        :param x: height coordinate.
        :param y: width coordinate.
        """
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class CellType(enum.Enum):
    """
        Class describing possible map cell content.
    """
    EMPTY_SPACE = ' '
    ROOM_SPACE = '.'
    VERTICAL_WALL = '-'
    HORIZONTAL_WALL = '|'
    DOOR = '*'
    PATH = '#'
    HERO = '@'
    ERROR = '倈'
