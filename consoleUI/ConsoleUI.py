# from tcod import tcod
import time

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
        self.__lifecicle(console)

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

    def __lifecicle(self, console):
        while not tcod.console_is_window_closed():
            if not self.__commandReceiver.is_empty():
                self.__make_command()
            self.__write_items(console, self.__items, self.__map)
            self.__write_inventory(console)
            self.__draw_map(self.__map.map, console)
            self.__draw_hero(self.__map.player.coordinate.x, self.__map.player.coordinate.y, console)
            self.__write_status(console, self.__map)
            self.__write_health(console, self.__map)
            tcod.console_flush()
            key = tcod.console_check_for_keypress()
            action = self.__handle_keys(key)
            if action is not None:
                self.__send_move(action)
            self.__ask_map()
            self.__ask_items()

    def __handle_keys(self, key):
        if key.vk == tcod.KEY_UP:
            return MoveType.UP
        elif key.vk == tcod.KEY_DOWN:
            return MoveType.DOWN
        elif key.vk == tcod.KEY_LEFT:
            return MoveType.LEFT
        elif key.vk == tcod.KEY_RIGHT:
            return MoveType.RIGHT
        elif key.vk in range(tcod.KEY_1, tcod.KEY_9 + 1):
            self.__selected_item = key.vk - tcod.KEY_1 + 1
        elif key.vk == tcod.KEY_CHAR:
            if key.c == ord('q') and 0 < self.__selected_item <= len(self.__items) \
                    or self.__selected_helmet or self.__selected_shirt or self.__selected_weapon:
                if key.c == ord('q') and 0 < self.__selected_item <= len(self.__items):
                    self.__send_item_action(ItemActionType.DROP, self.__items[self.__selected_item - 1])
                elif self.__selected_helmet:
                    self.__send_item_action(ItemActionType.DROP, self.__inventory.active_helmet)
                elif self.__selected_shirt:
                    self.__send_item_action(ItemActionType.DROP, self.__inventory.active_shirt)
                elif self.__selected_weapon:
                    self.__send_item_action(ItemActionType.DROP, self.__inventory.active_weapon)
            if key.c == ord('w') and 0 < self.__selected_item <= len(self.__items) \
                    or self.__selected_helmet or self.__selected_shirt or self.__selected_weapon:
                if key.c == ord('w') and 0 < self.__selected_item <= len(self.__items):
                    self.__send_item_action(ItemActionType.USE, self.__items[self.__selected_item - 1])
                elif self.__selected_helmet:
                    self.__send_item_action(ItemActionType.USE, self.__inventory.active_helmet)
                elif self.__selected_shirt:
                    self.__send_item_action(ItemActionType.USE, self.__inventory.active_shirt)
                elif self.__selected_weapon:
                    self.__send_item_action(ItemActionType.USE, self.__inventory.active_weapon)
            if key.c == ord('e') and 0 < self.__selected_item <= len(self.__items) \
                    or self.__selected_helmet or self.__selected_shirt or self.__selected_weapon:
                if key.c == ord('e') and 0 < self.__selected_item <= len(self.__items):
                    self.__send_item_action(ItemActionType.WEAR, self.__items[self.__selected_item - 1])
                elif self.__selected_helmet:
                    self.__send_item_action(ItemActionType.WEAR, self.__inventory.active_helmet)
                elif self.__selected_shirt:
                    self.__send_item_action(ItemActionType.WEAR, self.__inventory.active_shirt)
                elif self.__selected_weapon:
                    self.__send_item_action(ItemActionType.WEAR, self.__inventory.active_weapon)
            if key.c == ord('r') and 0 < self.__selected_item <= len(self.__items) \
                    or self.__selected_helmet or self.__selected_shirt or self.__selected_weapon:
                if key.c == ord('r') and 0 < self.__selected_item <= len(self.__items):
                    self.__send_item_action(ItemActionType.REMOVE_FROM_SLOT, self.__items[self.__selected_item - 1])
                elif self.__selected_helmet:
                    self.__send_item_action(ItemActionType.REMOVE_FROM_SLOT, self.__inventory.active_helmet)
                elif self.__selected_shirt:
                    self.__send_item_action(ItemActionType.REMOVE_FROM_SLOT, self.__inventory.active_shirt)
                elif self.__selected_weapon:
                    self.__send_item_action(ItemActionType.REMOVE_FROM_SLOT, self.__inventory.active_weapon)
            if key.c == ord('s'):
                self.__commandSender.put(SaveGame())
            if key.c == ord('l'):
                self.__commandSender.put(LoadGame())
            if key.c == ord('i') and self.__inventory.active_helmet:
                self.__selected_helmet = True
                self.__selected_shirt = False
                self.__selected_weapon = False
            if key.c == ord('o') and self.__inventory.active_shirt:
                self.__selected_helmet = False
                self.__selected_shirt = True
                self.__selected_weapon = False
            if key.c == ord('p') and self.__inventory.active_weapon:
                self.__selected_helmet = False
                self.__selected_shirt = False
                self.__selected_weapon = True
            return None
        else:
            return None

    @staticmethod
    def __draw_map(map_array, console):
        for i in range(len(map_array)):
            for j in range(len(map_array[i])):
                tcod.console_put_char(console, j, i, map_array[i][j], tcod.BKGND_NONE)

    @staticmethod
    def __draw_hero(pos_x, pos_y, console):
        tcod.console_put_char(console, pos_y, pos_x, CellType.HERO.value, tcod.BKGND_NONE)

    @staticmethod
    def __write_status(console, map):
        status = "STATUS:"
        padding = 0
        for s in status:
            tcod.console_put_char(console, padding, len(map.map) + 10, s, tcod.BKGND_NONE)
            padding += 1
        for s in map.status_message:
            tcod.console_put_char(console, padding, len(map.map) + 10, s, tcod.BKGND_NONE)
            padding += 1

    @staticmethod
    def __write_health(console, map):
        status = "HEALTH:"
        padding = 0
        for s in status + str(map.player.fight_stats.get_health()):
            tcod.console_put_char(console, padding, len(map.map) + 12, s, tcod.BKGND_NONE)
            padding += 1
        status = "STRENGTH:"
        padding = 0
        for s in status + str(map.player.fight_stats.get_strength()):
            tcod.console_put_char(console, padding, len(map.map) + 14, s, tcod.BKGND_NONE)
            padding += 1

    def __write_items(self, console, items, map):
        tcod.console_clear(console)
        padding_right = len(map.map) + 10
        padding_top = 0
        for ind, item in enumerate(items):
            if ind + 1 == self.__selected_item:
                self.__write_item(console, item, padding_right, padding_top, True)
            else:
                self.__write_item(console, item, padding_right, padding_top)
            padding_top += 1

    def __write_inventory(self, console):
        if not self.__inventory:
            return
        padding_top = len(self.__map.map) + 16
        if self.__inventory.active_helmet:
            self.__write_item(console, self.__inventory.active_helmet, 0, padding_top)
        if self.__inventory.active_shirt:
            self.__write_item(console, self.__inventory.active_shirt, 0, padding_top)
        if self.__inventory.active_weapon:
            self.__write_item(console, self.__inventory.active_weapon, 0, padding_top)

    @staticmethod
    def __write_item(console, item, padding_right, padding_top, selected=False):
        if selected:
            tcod.console_put_char(console, padding_right, padding_top, '*', tcod.BKGND_NONE)
            padding_right += 1
        for s in str(item.name):
            tcod.console_put_char(console, padding_right, padding_top, s, tcod.BKGND_NONE)
            padding_right += 1
