import enum


class MapConfig:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Map:
    def __init__(self, width, height, map_array):
        self.width = width
        self.height = height
        self.map_array = map_array

    def get_cell(self, height, width):
        return self.map_array[height][width] if 0 <= height < self.height and 0 <= width < self.width else CellType.ERROR


class CellType(enum.Enum):
    EMPTY_SPACE = ' '
    ROOM_SPACE = '.'
    VERTICAL_WALL = '|'
    HORIZONTAL_WALL = '-'
    DOOR = '*'
    PATH = '#'
    HERO = '@'
    ERROR = '倈'
