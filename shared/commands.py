from shared.common import Item
from shared.player_map import MoveType, ItemActions


class Command:
    """
        Abstract class for commands between ui and controller
    """


class MakeMove(Command):
    """
        Send controller user move
    """
    def __init__(self, move: MoveType):
        self.__move = move


class ActionsItem(Command):
    """
        Send controller user action with item
    """
    def __init__(self, action: ItemActions, item: Item):
        self.__action = action
        self.__item = item


class AskMap(Command):
    """
        Asking controller about map
    """


class AskItemsList(Command):
    """
        Asking controller about items list
    """
