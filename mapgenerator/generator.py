import random

from shared.common import CellType, Map

# from .shared.map import *

MIN_WIDTH = 4
MIN_HEIGHT = 4
MAX_WIDTH = 8
MAX_HEIGHT = 8


class Room:
    def __init__(self, cornerx, cornery, width, height):
        self.cornerx = cornerx
        self.cornery = cornery
        self.width = width
        self.height = height
        self.neighbours = []

    def getRightBorder(self):
        return self.cornerx + self.width + 1

    def getBottomBorder(self):
        return self.cornery + self.height + 1


def generateMap(config):
    field = [[CellType.EMPTY_SPACE] * config.width for i in range(config.height)]
    graph = generateRoomsGraph(config.width - 1, config.height - 1)
    field = printRoomsGraph(graph, field)
    result = Map(field, graph.cornerx + graph.width // 2, graph.cornery + graph.height // 2)
    return result


def printRoomsGraph(root, field):
    if (root == None):
        return field
    field = drawSingleRoom(field, root)
    for r in root.neighbours:
        field = printRoomsGraph(r, field)
    return field


def generateRoomsGraph(width, height, addx=0, addy=0):
    if (width <= MIN_WIDTH or height <= MIN_HEIGHT):
        return None
    room_width = random.randint(MIN_WIDTH, min(MAX_WIDTH, width - 1))
    room_height = random.randint(MIN_HEIGHT, min(MAX_HEIGHT, height - 1))
    room_x = random.randint(0, width - room_width)
    room_y = random.randint(0, height - room_height)
    room = Room(room_x, room_y, room_width, room_height)
    room.cornerx += addx
    room.cornery += addy
    left = generateRoomsGraph(room_x - 1, room_y + room_height - 1, addx, addy)
    right = generateRoomsGraph(width - room_width - room_x - 1, height - room_y - 1, addx + room_x + room_width,
                               addy + room_y)
    up = generateRoomsGraph(width - room_x - 1, room_y - 1, addx + room_x, addy)
    down = generateRoomsGraph(room_x + room_width - 1, height - room_y - room_height - 1, addx,
                              addy + room_y + room_height)
    room.neighbours = [left, right, up, down]
    return room


def drawSingleRoom(field, room):
    for j in range(room.height + 1):
        field[room.cornery + j][room.cornerx] = CellType.VERTICAL_WALL
        field[room.cornery + j][room.cornerx + room.width] = CellType.VERTICAL_WALL
    for i in range(room.width + 1):
        field[room.cornery][room.cornerx + i] = CellType.HORIZONTAL_WALL
        field[room.cornery + room.height][room.cornerx + i] = CellType.HORIZONTAL_WALL
    for i in range(1, room.width):
        for j in range(1, room.height):
            field[room.cornery + j][room.cornerx + i] = CellType.ROOM_SPACE
    return field


def printField(field):
    for line in field:
        for it in line:
            print(it.value, end="")
        print()
