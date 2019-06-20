from tcod import tcod

from shared.command import SaveGame, LoadGame
from shared.player_map import MoveType


class KeyHandler:
    ACTION_DROP = 1
    ACTION_USE = 2
    ACTION_WEAR = 3
    ACTION_REMOVE_FROM_SLOT = 4

    @staticmethod
    def handle_move_key(key):
        """
        convert key code into move
        :param key:
        :return:
        """
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
    def handle_inventory_position(key):
        """
        convert key code into inventory number
        :param key:
        :return:
        """
        if key.vk in range(tcod.KEY_1, tcod.KEY_9 + 1):
            return key.vk - tcod.KEY_1 + 1
        else:
            return None

    @staticmethod
    def handle_clothes(key, inventory):
        """
        convert key code into clothes inventory choose
        :param key:
        :param inventory:
        :return:
        """
        if key.c == ord('i') and inventory.active_helmet:
            return True, False, False
        if key.c == ord('o') and inventory.active_shirt:
            return False, True, False
        if key.c == ord('p') and inventory.active_weapon:
            return False, False, True

    @staticmethod
    def handle_game_state(key):
        """
        convert key code into game command
        :param key:
        :return:
        """
        if key.c == ord('s'):
            return SaveGame()
        elif key.c == ord('l'):
            return LoadGame()
        else:
            return None

    @staticmethod
    def handle_act(key):
        """
        convert key code into action
        :param key:
        :return:
        """
        if key.c == ord('q'):
            return KeyHandler.ACTION_DROP
        elif key.c == ord('w'):
            return KeyHandler.ACTION_USE
        elif key.c == ord('e'):
            return KeyHandler.ACTION_WEAR
        elif key.c == ord('r'):
            return KeyHandler.ACTION_REMOVE_FROM_SLOT
        else:
            return None
