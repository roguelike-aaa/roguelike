from tcod import tcod
import time

from shared.commands import AskMap, MakeMove, ActionsItem
from shared.common import Item, CellType
from shared.player_map import MoveType, ItemActions


class ConsoleUI:
    def __init__(self, commandReceiver, commandSender):
        self.__commandReceiver = commandReceiver
        self.__commandSender = commandSender
        self.__map = None

    def start(self, map):
        self.__map = self.__get_map_from_controller()
        screen_width = len(map.map) + 10
        screen_height = len(map.map[0]) + 20
        tcod.console_set_custom_font('arial12x12.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        console = tcod.console_init_root(screen_width, screen_height, 'Roguelike AAA', False)
        tcod.sys_set_fps(5)
        tcod.console_set_default_foreground(console, tcod.white)
        self.__lifecicle(console)

    def __get_map_from_controller(self):
        while self.__commandReceiver.is_empty():
            time.sleep(1)
        return self.__commandReceiver.pop()

    def __ask_map(self):
        self.__commandSender.push(AskMap())

    def __send_move(self, move: MoveType):
        self.__commandSender.push(MakeMove(move))

    def __send_item_action(self, action: ItemActions, item: Item):
        self.__commandSender.push(ActionsItem(action, item))

    def __make_command(self):
        pass

    def __lifecicle(self, console):
        while not tcod.console_is_window_closed():
            if not self.__commandReceiver.is_empty():
                self.__make_command()
            self.__draw_map(self.__map.map, console)
            self.__draw_hero(self.__map.player.coordinate.x, self.__map.player.coordinate.y, console)
            self.__write_status(console, self.__map)
            self.__write_health(console, self.__map)
            tcod.console_flush()
            key = tcod.console_check_for_keypress()
            action = self.__handle_keys(key)
            if action is not None:
                self.__send_move(action)

    @staticmethod
    def __handle_keys(key):
        if key.vk == tcod.KEY_UP:
            return MoveType.UP
        elif key.vk == tcod.KEY_DOWN:
            return MoveType.DOWN
        elif key.vk == tcod.KEY_LEFT:
            return MoveType.LEFT
        elif key.vk == tcod.KEY_RIGHT:
            return MoveType.RIGHT
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
        for s in status:
            tcod.console_put_char(console, padding, len(map.map) + 12, s, tcod.BKGND_NONE)
            padding += 1
        for s in str(map.player.fight_stats.current_health):
            tcod.console_put_char(console, padding, len(map.map) + 12, s, tcod.BKGND_NONE)
            padding += 1

