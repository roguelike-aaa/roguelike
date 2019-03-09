import enum


class Map:
    def __init__(self, height, width, map_array):
        self.width = width
        self.height = height
        self.map_array = map_array

    def get_cell(self, height, width):
        return self.map_array[height][width] if 0 <= height < self.height and 0 <= width < self.width else CellType.ERROR


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class CellType(enum.Enum):
    EMPTY_SPACE = ' '
    ROOM_SPACE = '.'
    VERTICAL_WALL = '|'
    HORIZONTAL_WALL = '-'
    DOOR = '*'
    PATH = '#'
    HERO = '@'
    ERROR = '倈'
