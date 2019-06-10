import unittest

from controller.session import Session
from shared.common import *
from shared.player_map import *
from shared.map_init import *


class TestSession(unittest.TestCase):
    def setUp(self):
        self.player_token = PlayerToken("pupa")
        self.map = Map(3, 5, [
            [CellType.EMPTY_SPACE, CellType.EMPTY_SPACE, CellType.HORIZONTAL_WALL, CellType.HORIZONTAL_WALL,
             CellType.EMPTY_SPACE],
            [CellType.PATH, CellType.DOOR, CellType.ROOM_SPACE, CellType.ROOM_SPACE, CellType.VERTICAL_WALL],
            [CellType.PATH, CellType.EMPTY_SPACE, CellType.HORIZONTAL_WALL, CellType.HORIZONTAL_WALL,
             CellType.EMPTY_SPACE]
        ])
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(5, 3))], self.map)

    def test_create_session(self):
        Session([Player(Coordinate(0, 0), self.player_token, CurrentFightStats(2, 1))],
                Map(1, 1, [[CellType.ROOM_SPACE]]), [], [])

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
        self.assertEqual(Coordinate(1, 3),
                         self.session.game_content.players_by_token[self.player_token].data.coordinate)

    def test_player_move_denied(self):
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.DOWN)))
        self.assertEqual(Coordinate(1, 2),
                         self.session.game_content.players_by_token[self.player_token].data.coordinate)

    def test_player_move_on_door(self):
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.assertEqual(Coordinate(1, 1),
                         self.session.game_content.players_by_token[self.player_token].data.coordinate)

    def test_player_move_on_door_map(self):
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.assertEqual([
            '  -- ',
            '#*..|',
            '  -- '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_player_move_on_path(self):
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.assertEqual(Coordinate(1, 0),
                         self.session.game_content.players_by_token[self.player_token].data.coordinate)

    def test_player_move_on_path_map(self):
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.assertEqual([
            '  -- ',
            '#*..|',
            '# -- '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_player_spawns_on_door(self):
        self.session = Session([Player(Coordinate(1, 1), self.player_token, CurrentFightStats(1, 3))], self.map)
        self.assertEqual([
            '  -- ',
            '#*..|',
            '  -- '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_player_spawns_on_path(self):
        self.session = Session([Player(Coordinate(2, 0), self.player_token, CurrentFightStats(3, 5))], self.map)
        self.assertEqual([
            '     ',
            '#    ',
            '#    '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_player_spawns_on_path_near_door(self):
        self.session = Session([Player(Coordinate(1, 0), self.player_token, CurrentFightStats(6, 8))], self.map)
        self.assertEqual([
            '     ',
            '#*   ',
            '#    '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_mob_on_map(self):
        self.session = Session([], self.map, [Mob(Coordinate(1, 2), ModMode.PASSIVE, CurrentFightStats(6, 3))])
        self.assertEqual([
            '  -- ',
            '#*%.|',
            '# -- '], list(map(lambda x: "".join(x), self.session.dump_map())))

    def test_mob_aggressive_movement(self):
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(6, 8))],
                               self.map, [Mob(Coordinate(1, 3), ModMode.AGGRESSIVE, CurrentFightStats(6, 3))])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.assertEqual([
            '  -- ',
            '#*%.|',
            '# -- '], list(map(lambda x: "".join(x), self.session.dump_map())))

    def test_mob_passive_movement(self):
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(6, 8))],
                               self.map, [Mob(Coordinate(1, 3), ModMode.PASSIVE, CurrentFightStats(6, 3))])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.assertEqual([
            '  -- ',
            '#*.%|',
            '# -- '], list(map(lambda x: "".join(x), self.session.dump_map())))

    def test_mob_frightened_movement(self):
        self.session = Session([Player(Coordinate(1, 0), self.player_token, CurrentFightStats(6, 8))],
                               self.map, [Mob(Coordinate(1, 2), ModMode.FRIGHTENED, CurrentFightStats(6, 3))])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        self.assertEqual([
            '  -- ',
            '#*.%|',
            '# -- '], list(map(lambda x: "".join(x), self.session.dump_map())))

    def test_mob_aggressive_attack(self):
        self.session = Session([Player(Coordinate(1, 1), self.player_token, CurrentFightStats(6, 8))],
                               self.map, [Mob(Coordinate(1, 3), ModMode.AGGRESSIVE, CurrentFightStats(6, 3))])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        player = self.session.game_content.players_by_token[self.player_token]
        self.assertEqual(Coordinate(1, 2), player.data.coordinate)
        self.assertEqual([
            '  -- ',
            '#*.%|',
            '# -- '], list(map(lambda x: "".join(x), self.session.dump_map())))
        self.assertEqual(3, player.data.fight_stats.get_health())

    def test_kill_mob(self):
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(6, 8))],
                               self.map, [Mob(Coordinate(1, 3), ModMode.AGGRESSIVE, CurrentFightStats(6, 3))])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        player = self.session.game_content.players_by_token[self.player_token]
        self.assertEqual(Coordinate(1, 2), player.data.coordinate)
        self.assertEqual([
            '  -- ',
            '#*..|',
            '# -- '], list(map(lambda x: "".join(x), self.session.dump_map())))

    def test_kill_player(self):
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(3, 1))],
                               self.map, [Mob(Coordinate(1, 3), ModMode.AGGRESSIVE, CurrentFightStats(6, 3))])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        self.assertEqual("You are dead", self.session.game_content.players_by_token[self.player_token].status)
        self.assertEqual([
            '  -- ',
            '#*.%|',
            '# -- '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_item_in_sight(self):
        self.session = Session([Player(Coordinate(1, 1), self.player_token, CurrentFightStats(3, 1))],
                               self.map,
                               items=[ItemInitState(Coordinate(1, 3), BodyCloth(Bonus(1, 1), "Foo"))])
        self.assertEqual([
            '  -- ',
            '#*.!|',
            '  -- '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_item_out_of_sight(self):
        self.session = Session([Player(Coordinate(1, 3), self.player_token, CurrentFightStats(3, 1))],
                               self.map,
                               items=[ItemInitState(Coordinate(1, 0), BodyCloth(Bonus(1, 1), "Foo"))])
        self.assertEqual([
            '  -- ',
            ' *..|',
            '  -- '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_picking_item(self):
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(3, 1))],
                               self.map,
                               items=[ItemInitState(Coordinate(1, 3), BodyCloth(Bonus(1, 2), "Foo")),
                                      ItemInitState(Coordinate(1, 1), BodyCloth(Bonus(1, 0), "Bar"))])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        new_items = list(self.session.game_content.players_by_token[self.player_token].data.inventory.items.values())
        self.assertEqual(1, len(new_items))

        self.assertEqual(Bonus(1, 2), new_items[0].bonus)

        self.assertEqual([
            '  -- ',
            ' !..|',
            '  -- '], list(map(lambda x: "".join(x), self.session.dump_players_map(self.player_token))))

    def test_wearing_shirt(self):
        item = ItemInitState(Coordinate(1, 3), BodyCloth(Bonus(1, 2), "Foo"))
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(2, 1))],
                               self.map,
                               items=[item])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        self.session.change_player_state(self.player_token, StateChange(ItemAction(ItemActionType.WEAR, item.item)))

        player = self.session.game_content.players_by_token[self.player_token]

        inventory = player.data.inventory
        new_items = list(inventory.items.values())
        self.assertEqual(0, len(new_items))

        self.assertEqual(2, player.data.fight_stats.get_health())
        self.assertEqual(3, player.data.fight_stats.get_strength())
        self.assertEqual(Bonus(1, 2), inventory.active_shirt.bonus)

    def test_wearing_helmet(self):
        item = ItemInitState(Coordinate(1, 3), HeadCloth(Bonus(1, 2), "Foo"))
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(2, 1))],
                               self.map,
                               items=[item])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        self.session.change_player_state(self.player_token, StateChange(ItemAction(ItemActionType.WEAR, item.item)))
        player = self.session.game_content.players_by_token[self.player_token]

        inventory = player.data.inventory
        new_items = list(inventory.items.values())
        self.assertEqual(0, len(new_items))

        self.assertEqual(2, player.data.fight_stats.get_health())
        self.assertEqual(3, player.data.fight_stats.get_strength())
        self.assertEqual(Bonus(1, 2), inventory.active_helmet.bonus)

    def test_wearing_weapon(self):
        item = ItemInitState(Coordinate(1, 3), Weapon(Bonus(1, 2), "Foo"))
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(2, 1))],
                               self.map,
                               items=[item])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        self.session.change_player_state(self.player_token, StateChange(ItemAction(ItemActionType.WEAR, item.item)))
        player = self.session.game_content.players_by_token[self.player_token]

        inventory = player.data.inventory
        new_items = list(inventory.items.values())
        self.assertEqual(0, len(new_items))

        self.assertEqual(2, player.data.fight_stats.get_health())
        self.assertEqual(3, player.data.fight_stats.get_strength())
        self.assertEqual(Bonus(1, 2), inventory.active_weapon.bonus)

    def test_taking_off_shirt(self):
        item = ItemInitState(Coordinate(1, 3), BodyCloth(Bonus(1, 2), "Foo"))
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(3, 1))],
                               self.map,
                               items=[item])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        self.session.change_player_state(self.player_token, StateChange(ItemAction(ItemActionType.WEAR, item.item)))
        self.session.change_player_state(self.player_token, StateChange(ItemAction(ItemActionType.REMOVE_FROM_SLOT, item.item)))
        player = self.session.game_content.players_by_token[self.player_token]

        inventory = player.data.inventory
        new_items = list(inventory.items.values())
        self.assertEqual(1, len(new_items))
        self.assertEqual(3, player.data.fight_stats.get_health())
        self.assertEqual(1, player.data.fight_stats.get_strength())
        self.assertEqual(None, inventory.active_shirt)

    def test_taking_off_helmet(self):
        item = ItemInitState(Coordinate(1, 3), HeadCloth(Bonus(1, 2), "Foo"))
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(3, 1))],
                               self.map,
                               items=[item])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        self.session.change_player_state(self.player_token, StateChange(ItemAction(ItemActionType.WEAR, item.item)))
        self.session.change_player_state(self.player_token, StateChange(ItemAction(ItemActionType.REMOVE_FROM_SLOT, item.item)))
        player = self.session.game_content.players_by_token[self.player_token]

        inventory = player.data.inventory
        new_items = list(inventory.items.values())
        self.assertEqual(1, len(new_items))
        self.assertEqual(3, player.data.fight_stats.get_health())
        self.assertEqual(1, player.data.fight_stats.get_strength())
        self.assertEqual(None, inventory.active_helmet)

    def test_taking_off_weapon(self):
        item = ItemInitState(Coordinate(1, 3), Weapon(Bonus(1, 2), "Foo"))
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(3, 1))],
                               self.map,
                               items=[item])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        self.session.change_player_state(self.player_token, StateChange(ItemAction(ItemActionType.WEAR, item.item)))
        self.session.change_player_state(self.player_token, StateChange(ItemAction(ItemActionType.REMOVE_FROM_SLOT, item.item)))
        player = self.session.game_content.players_by_token[self.player_token]

        inventory = player.data.inventory
        new_items = list(inventory.items.values())
        self.assertEqual(1, len(new_items))

        self.assertEqual(3, player.data.fight_stats.get_health())
        self.assertEqual(1, player.data.fight_stats.get_strength())
        self.assertEqual(None, inventory.active_weapon)

    def test_dropping_item(self):
        item = ItemInitState(Coordinate(1, 3), Weapon(Bonus(1, 2), "Foo"))
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(3, 1))],
                               self.map,
                               items=[item])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.session.change_player_state(self.player_token, StateChange(ItemAction(ItemActionType.DROP, item.item)))
        player = self.session.game_content.players_by_token[self.player_token]

        inventory = player.data.inventory
        new_items = list(inventory.items.values())
        self.assertEqual(0, len(new_items))

        self.assertEqual([
            '  -- ',
            '#*!.|',
            '# -- '], list(map(lambda x: "".join(x), self.session.dump_map())))

    def test_drinking_potion(self):
        item = ItemInitState(Coordinate(1, 3), Potion(Bonus(1, 2), "Foo"))
        self.session = Session([Player(Coordinate(1, 2), self.player_token, CurrentFightStats(2, 1))],
                               self.map,
                               items=[item])
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.RIGHT)))
        self.session.change_player_state(self.player_token, StateChange(PlayerMove(MoveType.LEFT)))
        self.session.change_player_state(self.player_token, StateChange(ItemAction(ItemActionType.USE, item.item)))
        player = self.session.game_content.players_by_token[self.player_token]

        inventory = player.data.inventory
        new_items = list(inventory.items.values())
        self.assertEqual(0, len(new_items))

        self.assertEqual(2, player.data.fight_stats.get_health())
        self.assertEqual(3, player.data.fight_stats.get_strength())
        self.assertEqual(None, inventory.active_weapon)