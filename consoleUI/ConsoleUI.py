from tcod import tcod

from controller.map_controller import MapController
from shared.map import CellType
from shared.state_change import MoveType


class ConsoleUI:
    def __init__(self):
        pass

    def start(self, map):
        screen_width = len(map.map_array)
        screen_height = len(map.map_array[0])

        console = tcod.console_init_root(screen_width, screen_height, 'roguelike aaa', False)
        tcod.sys_set_fps(5)
        tcod.console_set_default_foreground(0, tcod.white)
        self._draw(console)

    def _draw_map(self, map_array, console):
        for i in range(len(map_array)):
            for j in range(len(map_array[i])):
                tcod.console_put_char(console, i, j, map_array[i][j], tcod.BKGND_NONE)

    def _draw_hero(self, pos_x, pos_y, console):
        tcod.console_put_char(console, pos_x, pos_y, CellType.HERO, tcod.BKGND_NONE)

    def _draw(self, console):
        while not tcod.console_is_window_closed():
            map_ = MapController.get_map()
            self._draw_map(map_.map_array, console)
            self._draw_hero(map_.pos_x, map_.pos_y, console)
            tcod.console_flush()
            key = tcod.console_check_for_keypress()
            action = self._handle_keys(key)
            MapController.change_state(action)

    def _handle_keys(self, key):
        if key.vk == tcod.KEY_UP:
            return MoveType.UP
        elif key.vk == tcod.KEY_DOWN:
            return MoveType.DOWN
        elif key.vk == tcod.KEY_LEFT:
            return MoveType.LEFT
        elif key.vk == tcod.KEY_RIGHT:
            return MoveType.RIGHT


