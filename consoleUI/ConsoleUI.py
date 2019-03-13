from tcod import tcod

from controller.map_controller import MapController
from shared.common import CellType
from shared.player_map import MoveType, StateChange, PlayerMove, PlayerToken


class ConsoleUI:
    def __init__(self, player_token, controller):
        self.__player_token = player_token
        self.__controller = controller

    def start(self):
        map = self.__controller.get_player_map(self.__player_token)
        screen_width = len(map.map) + 10
        screen_height = len(map.map[0]) + 10
        tcod.console_set_custom_font('arial12x12.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        console = tcod.console_init_root(screen_width, screen_height, 'Roguelike AAA', False)
        tcod.sys_set_fps(5)
        tcod.console_set_default_foreground(console, tcod.white)
        self._draw(console)

    def _draw_map(self, map_array, console):
        for i in range(len(map_array)):
            for j in range(len(map_array[i])):
                tcod.console_put_char(console, j, i, map_array[j][i], tcod.BKGND_NONE)

    def _draw_hero(self, pos_x, pos_y, console):
        tcod.console_put_char(console, pos_x, pos_y, CellType.HERO.value, tcod.BKGND_NONE)

    def _draw(self, console):
        while not tcod.console_is_window_closed():
            map_ = self.__controller.get_player_map(self.__player_token)
            self._draw_map(map_.map, console)
            self._draw_hero(map_.player.coordinate.x, map_.player.coordinate.y, console)
            tcod.console_flush()
            key = tcod.console_check_for_keypress()
            action = self._handle_keys(key)
            if action is not None:
                self.__controller.change_state(StateChange(PlayerMove(action)), self.__player_token)

    def _handle_keys(self, key):
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
