import random

from shared.common import CellType, Map, Coordinate
from shared.map_init import GeneratedMap, PlayerInitState
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

    def get_right_border(self):
        return self.cornerx + self.width

    def get_bottom_border(self):
        return self.cornery + self.height


def generate_map(config):
    field = [[CellType.EMPTY_SPACE] * config.width for i in range(config.height)]
    graph = generate_rooms_graph(config.width - 1, config.height - 1)
    field = print_rooms_graph(graph, field)
    field = draw_paths(graph, field)
    person = PlayerInitState(Coordinate(graph.cornerx + graph.width // 2, graph.cornery + graph.height // 2))
    result = Map(config.height, config.width, field)
    return GeneratedMap(result, person)

def draw_paths(graph, field):
    for child in graph.neighbours:
        if (child != None):
            field = draw_path_between_two_rooms(field, child, graph)
            field = draw_paths(child, field)
    return field


def draw_path_between_two_rooms(field, room1, room2):
    if (room1.cornerx > room2.cornerx):
        room1, room2 = room2, room1
    if (abs(room1.cornery - room2.cornery) <= room1.height and abs(room1.cornery - room2.cornery) <= room2.height):
        return draw_single_path(field, room1.get_right_border(), room1.cornery + room1.height // 2, room2.cornerx, room2.cornery + room2.height // 2)
    if (room1.cornery < room2.cornery):
        return draw_single_path(field, room1.cornerx + room1.width // 2, room1.get_bottom_border(), room2.cornerx + room2.width // 2, room2.cornery)
    return draw_single_path(field, room1.cornerx + room1.width // 2, room1.cornery, room2.cornerx + room2.width // 2, room2.get_bottom_border())
            

def draw_single_path(field, x1, y1, x2, y2):
    field[y1][x1] = CellType.DOOR
    field[y2][x2] = CellType.DOOR
    if (abs(x1 - x2) + abs(y1 - y2) == 1):
        return field
    cx = x1
    cy = y1
    while (abs(cx - x2) + abs(cy - y2) > 1):
        if (random.randint(0, abs(cx - x2) + abs(cy - y2) - 1) < abs(cx - x2)):
            cx += (x2 - cx) // abs(x2 - cx)
        else:
            cy += (y2 - cy) // abs(y2 - cy)
        if (field[cy][cx] == CellType.VERTICAL_WALL or field[cy][cx] == CellType.HORIZONTAL_WALL):
            field[cy][cx] = CellType.DOOR
        elif (field[cy][cx] == CellType.EMPTY_SPACE or field[cy][cx] == CellType.PATH):
            field[cy][cx] = CellType.PATH
        else:
            return field
    return field

def print_rooms_graph(root, field):
    if (root == None):
        return field
    field = draw_single_room(field, root)
    for r in root.neighbours:
        field = print_rooms_graph(r, field)
    return field


def generate_rooms_graph(width, height, addx=0, addy=0):
    if (width <= MIN_WIDTH or height <= MIN_HEIGHT):
        return None
    room_width = random.randint(MIN_WIDTH, min(MAX_WIDTH, width - 1))
    room_height = random.randint(MIN_HEIGHT, min(MAX_HEIGHT, height - 1))
    room_x = random.randint(0, width - room_width)
    room_y = random.randint(0, height - room_height)
    room = Room(room_x, room_y, room_width, room_height)
    room.cornerx += addx
    room.cornery += addy
    left = generate_rooms_graph(room_x - 1, room_y + room_height - 1, addx, addy)
    right = generate_rooms_graph(width - room_width - room_x - 1, height - room_y - 1, addx + room_x + room_width + 1,
                               addy + room_y + 1)
    up = generate_rooms_graph(width - room_x - 1, room_y - 1, addx + room_x + 1, addy)
    down = generate_rooms_graph(room_x + room_width - 1, height - room_y - room_height - 1, addx,
                              addy + room_y + room_height + 1)
    room.neighbours = [left, right, up, down]
    return room


def draw_single_room(field, room):
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


def print_field(field):
    for line in field:
        for it in line:
            print(it.value, end="")
        print()
