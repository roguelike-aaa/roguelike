import enum


class MapConfig:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Map:
    def __init__(self, map_array):
        self.map_array = map_array


class CellType(enum.Enum):
    EMPTY_SPACE = ' '
    ROOM_SPACE = '.'
    VERTICAL_WALL = '|'
    HORIZONTAL_WALL = '-'
    DOOR = '*'
    PATH = '#'
    HERO = '@'
