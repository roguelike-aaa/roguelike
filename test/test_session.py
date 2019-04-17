import unittest

from controller.session import Session
from shared.common import CellType, Coordinate, Map
from shared.player_map import Player, PlayerToken, MoveType, PlayerMove, StateChange, CurrentFightStats


class TestSession(unittest.TestCase):
    def setUp(self):
        self.player_token = PlayerToken("pupa")
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(5, 10, 3))], Map(3, 5, [
            [CellType.EMPTY_SPACE, CellType.EMPTY_SPACE, CellType.HORIZONTAL_WALL, CellType.HORIZONTAL_WALL,
             CellType.EMPTY_SPACE],
            [CellType.PATH, CellType.DOOR, CellType.ROOM_SPACE, CellType.ROOM_SPACE, CellType.VERTICAL_WALL],
            [CellType.PATH, CellType.EMPTY_SPACE, CellType.HORIZONTAL_WALL, CellType.HORIZONTAL_WALL,
             CellType.EMPTY_SPACE]
        ]), [])

    def test_create_session(self):
        Session([Player(Coordinate(0, 0), self.player_token, CurrentFightStats(2, 3, 1))],
                Map(1, 1, [[CellType.ROOM_SPACE]]), [])

    def test_dump_player_map(self):
        self.assertEqual([
            '  -- ',
            ' *..|',
            '  -- '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_dump_full_map(self):
        self.assertEqual([
            '  -- ',
            '#*..|',
            '# -- '], list(map(lambda x: "".join(x), self.session.dump_map())))

    def test_player_simple_move(self):
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        self.assertEqual(Coordinate(1, 3), self.session.game_content.players_by_token[self.player_token].data.coordinate)

    def test_player_move_denied(self):
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.DOWN)))
        self.assertEqual(Coordinate(1, 2), self.session.game_content.players_by_token[self.player_token].data.coordinate)

    def test_player_move_on_door(self):
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.assertEqual(Coordinate(1, 1), self.session.game_content.players_by_token[self.player_token].data.coordinate)

    def test_player_move_on_door_map(self):
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.assertEqual([
            '  -- ',
            '#*..|',
            '  -- '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_player_move_on_path(self):
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.assertEqual(Coordinate(1, 0), self.session.game_content.players_by_token[self.player_token].data.coordinate)

    def test_player_move_on_path_map(self):
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.assertEqual([
            '  -- ',
            '#*..|',
            '# -- '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_player_spawns_on_door(self):
        self.session = Session([Player(Coordinate(1, 1), self.player_token, CurrentFightStats(1, 2, 3))], Map(3, 5, [
            [CellType.EMPTY_SPACE, CellType.EMPTY_SPACE, CellType.HORIZONTAL_WALL, CellType.HORIZONTAL_WALL,
             CellType.EMPTY_SPACE],
            [CellType.PATH, CellType.DOOR, CellType.ROOM_SPACE, CellType.ROOM_SPACE, CellType.VERTICAL_WALL],
            [CellType.PATH, CellType.EMPTY_SPACE, CellType.HORIZONTAL_WALL, CellType.HORIZONTAL_WALL,
             CellType.EMPTY_SPACE]
        ]), [])
        self.assertEqual([
            '  -- ',
            '#*..|',
            '  -- '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_player_spawns_on_path(self):
        self.session = Session([Player(Coordinate(2, 0), self.player_token, CurrentFightStats(3, 4, 5))], Map(3, 5, [
            [CellType.EMPTY_SPACE, CellType.EMPTY_SPACE, CellType.HORIZONTAL_WALL, CellType.HORIZONTAL_WALL,
             CellType.EMPTY_SPACE],
            [CellType.PATH, CellType.DOOR, CellType.ROOM_SPACE, CellType.ROOM_SPACE, CellType.VERTICAL_WALL],
            [CellType.PATH, CellType.EMPTY_SPACE, CellType.HORIZONTAL_WALL, CellType.HORIZONTAL_WALL,
             CellType.EMPTY_SPACE]
        ]), [])
        self.assertEqual([
            '     ',
            '#    ',
            '#    '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_player_spawns_on_path_near_door(self):
        self.session = Session([Player(Coordinate(1, 0), self.player_token, CurrentFightStats(6, 7, 8))], Map(3, 5, [
            [CellType.EMPTY_SPACE, CellType.EMPTY_SPACE, CellType.HORIZONTAL_WALL, CellType.HORIZONTAL_WALL,
             CellType.EMPTY_SPACE],
            [CellType.PATH, CellType.DOOR, CellType.ROOM_SPACE, CellType.ROOM_SPACE, CellType.VERTICAL_WALL],
            [CellType.PATH, CellType.EMPTY_SPACE, CellType.HORIZONTAL_WALL, CellType.HORIZONTAL_WALL,
             CellType.EMPTY_SPACE]
        ]), [])
        self.assertEqual([
            '     ',
            '#*   ',
            '#    '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))
