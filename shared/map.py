import enum


class MapConfig:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Map:
    def __init__(self, map_array, pos_x, pos_y):
        self.map_array = map_array
        self.pos_x = pos_x
        self.pos_y = pos_y

class CellType(enum.Enum):
    EMPTY_SPACE = ' '
    ROOM_SPACE = '.'
    VERTICAL_WALL = '|'
    HORIZONTAL_WALL = '-'
    DOOR = '*'
    PATH = '#'
    HERO = '@'
