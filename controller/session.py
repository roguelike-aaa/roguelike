import collections

from shared.map import *
from shared.player_map import *
from shared.state_change import MoveType


class Session:
    def __init__(self, player_tokens, map_settings):
        self.players = {}

        # TODO: call map generator
        self.map = Map(5, 5, [[CellType.ROOM_SPACE] * 5] * 5)
        for player in player_tokens:
            self.players[player] = PlayerState(self.map)

    def change_player_state(self, player_token, state_change):
        self.players[player_token].change_state(state_change)

    def dump_map(self, mask=None):
        result_map = []
        for i in range(self.map.height):
            result_map.append([])
            for j in range(self.map.width):
                result_map[-1].append(
                    (self.map.get_cell(i, j) if mask[i][j] or mask is None else CellType.EMPTY_SPACE).value)
        return result_map

    def dump_players_map(self, players_token):
        return self.dump_map(self.players[players_token].mask)


class SinglePlayerSession(Session):
    def __init__(self, player_token, map_settings):
        super().__init__([player_token], map_settings)


class PlayerState:
    def __init__(self, game_map, player):
        self.map = game_map
        self.mask = [[0 for _ in range(game_map.width)] for _ in range(game_map.height)]
        self.coordinate = player.coordinate
        self.update_visible_area()

    def change_state(self, state_change):
        new_coordinate = self.coordinate + {
            MoveType.DOWN:  (1,  0),
            MoveType.UP:    (-1, 0),
            MoveType.RIGHT: (0,  1),
            MoveType.LEFT:  (0, -1),
        }[state_change.player_move.move_type]
        if self.map.get_cell(new_coordinate) in [CellType.DOOR, CellType.ROOM_SPACE, CellType.PATH]:
            self.coordinate = new_coordinate
            self.update_visible_area()

    def update_visible_area(self):
        queue = collections.deque([self.coordinate])
        self.mask[self.coordinate.x][self.coordinate.y] = 1

        deltas = [Coordinate(0, 1),
                  Coordinate(0, -1),
                  Coordinate(1, 0),
                  Coordinate(-1, 0)]

        queue.append(self.coordinate)
        while queue:
            coordinate = queue.pop()
            for delta in deltas:
                new_coordinate = coordinate + delta
                new_cell = self.map.get_cell(new_coordinate.x, new_coordinate.y)

                if new_cell in [CellType.ERROR, CellType.EMPTY_SPACE]:
                    continue
                self.mask[new_coordinate.x][new_coordinate.y] = 1
                if new_cell is CellType.ROOM_SPACE:
                    queue.appendleft(new_coordinate)
