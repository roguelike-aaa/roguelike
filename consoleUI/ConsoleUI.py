from tcod import tcod
import time

from consoleUI.KeyHandler import KeyHandler
from shared.command import AskMap, ChangeState, SendMap, SendItemsList, AskItemsList, SaveGame, LoadGame
from shared.common import Item, CellType
from shared.player_map import MoveType, ItemActionType, StateChange, PlayerMove, ItemAction


class ConsoleUI:
    def __init__(self, commandReceiver, commandSender):
        self.__commandReceiver = commandReceiver
        self.__commandSender = commandSender
        self.__map = None
        self.__items = []
        self.__selected_item = 0
        self.__inventory = None
        self.__selected_helmet = False
        self.__selected_shirt = False
        self.__selected_weapon = False
        self.__console = None

    def start(self):
        """
            Start UI
        """
        self.__map = self.__get_map_from_controller().map
        screen_width = len(self.__map.map) + 50
        screen_height = len(self.__map.map[0]) + 20
        tcod.console_set_custom_font('arial12x12.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        console = tcod.console_init_root(screen_width, screen_height, 'Roguelike AAA', False)
        tcod.sys_set_fps(5)
        tcod.console_set_default_foreground(console, tcod.white)
        self.__console = console
        self.__lifecicle()

    def __get_map_from_controller(self):
        self.__ask_map()
        while self.__commandReceiver.is_empty():
            time.sleep(1)
        return self.__commandReceiver.pop()

    def __ask_map(self):
        self.__commandSender.put(AskMap())

    def __ask_items(self):
        self.__commandSender.put(AskItemsList())

    def __send_move(self, move: MoveType):
        self.__commandSender.put(ChangeState(StateChange(PlayerMove(move))))

    def __send_item_action(self, action: ItemActionType, item: Item):
        self.__commandSender.put(ChangeState(StateChange(ItemAction(action, item))))

    def __make_command(self):
        while not self.__commandReceiver.is_empty():
            command = self.__commandReceiver.pop()
            if command.__class__ == SendMap:
                self.__map = command.map
            elif command.__class__ == SendItemsList:
                self.__items = list(command.items.items.values())
                self.__inventory = command.items

    def __lifecicle(self):
        while not tcod.console_is_window_closed():
            if not self.__commandReceiver.is_empty():
                self.__make_command()
            self.__write_items(self.__items, self.__map)
            self.__write_inventory()
            self.__draw_map(self.__map.map)
            self.__draw_hero(self.__map.player.coordinate.x, self.__map.player.coordinate.y)
            self.__write_status(self.__map)
            self.__write_health(self.__map)
            tcod.console_flush()
            key = tcod.console_check_for_keypress()
            action = self.__handle_keys(key)
            if action is not None:
                self.__send_move(action)
            self.__ask_map()
            self.__ask_items()

    def __handle_keys(self, key):
        res = KeyHandler.handle_move_key(key)
        if res is not None:
            return res

        res = KeyHandler.handle_inventory_position(key)
        if res is not None:
            self.__selected_item = res

        if key.vk == tcod.KEY_CHAR:
            res = KeyHandler.handle_clothes(key, self.__inventory)
            if res is not None:
                self.__selected_helmet, self.__selected_shirt, self.__selected_weapon = res

            res = KeyHandler.handle_act(key)
            if res is not None:
                self.__make_actions(res)

            res = KeyHandler.handle_game_state(key)
            if res is not None:
                self.__commandSender.put(res)

    def __make_actions(self, key):
        action = KeyHandler.handle_act(key)
        if action is None and not (0 < self.__selected_item <= len(self.__items)
                                   or self.__selected_helmet or self.__selected_shirt or self.__selected_weapon):
            return
        if action == KeyHandler.ACTION_DROP:
            self.__make_action(ItemActionType.DROP)
        elif action == KeyHandler.ACTION_WEAR:
            self.__make_action(ItemActionType.WEAR)
        elif action == KeyHandler.ACTION_USE:
            self.__make_action(ItemActionType.USE)
        elif action == KeyHandler.ACTION_REMOVE_FROM_SLOT:
            self.__make_action(ItemActionType.ACTION_REMOVE_FROM_SLOT)

    def __make_action(self, type):
        if 0 < self.__selected_item <= len(self.__items):
            self.__send_item_action(type, self.__items[self.__selected_item - 1])
        elif self.__selected_helmet:
            self.__send_item_action(type, self.__inventory.active_helmet)
        elif self.__selected_shirt:
            self.__send_item_action(type, self.__inventory.active_shirt)
        elif self.__selected_weapon:
            self.__send_item_action(type, self.__inventory.active_weapon)

    def __draw_map(self, map_array):
        for i in range(len(map_array)):
            for j in range(len(map_array[i])):
                tcod.console_put_char(self.__console, j, i, map_array[i][j], tcod.BKGND_NONE)

    def __draw_hero(self, pos_x, pos_y):
        tcod.console_put_char(self.__console, pos_y, pos_x, CellType.HERO.value, tcod.BKGND_NONE)

    def __write_status(self, map):
        status = "STATUS:"
        padding = 0
        for s in status:
            tcod.console_put_char(self.__console, padding, len(map.map) + 10, s, tcod.BKGND_NONE)
            padding += 1
        for s in map.status_message:
            tcod.console_put_char(self.__console, padding, len(map.map) + 10, s, tcod.BKGND_NONE)
            padding += 1

    def __write_health(self, map):
        status = "HEALTH:"
        padding = 0
        for s in status + str(map.player.fight_stats.get_health()):
            tcod.console_put_char(self.__console, padding, len(map.map) + 12, s, tcod.BKGND_NONE)
            padding += 1
        status = "STRENGTH:"
        padding = 0
        for s in status + str(map.player.fight_stats.get_strength()):
            tcod.console_put_char(self.__console, padding, len(map.map) + 14, s, tcod.BKGND_NONE)
            padding += 1

    def __write_items(self, items, map):
        tcod.console_clear(self.__console)
        padding_right = len(map.map) + 10
        padding_top = 0
        for ind, item in enumerate(items):
            if ind + 1 == self.__selected_item:
                self.__write_item(item, padding_right, padding_top, True)
            else:
                self.__write_item(item, padding_right, padding_top)
            padding_top += 1

    def __write_inventory(self):
        if not self.__inventory:
            return
        padding_top = len(self.__map.map) + 16
        if self.__inventory.active_helmet:
            self.__write_item(self.__inventory.active_helmet, 0, padding_top)
        if self.__inventory.active_shirt:
            self.__write_item(self.__inventory.active_shirt, 0, padding_top)
        if self.__inventory.active_weapon:
            self.__write_item(self.__inventory.active_weapon, 0, padding_top)

    def __write_item(self, item, padding_right, padding_top, selected=False):
        if selected:
            tcod.console_put_char(self.__console, padding_right, padding_top, '*', tcod.BKGND_NONE)
            padding_right += 1
        for s in str(item.name):
            tcod.console_put_char(self.__console, padding_right, padding_top, s, tcod.BKGND_NONE)
            padding_right += 1
