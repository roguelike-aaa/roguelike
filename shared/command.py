import queue
from abc import ABC

from shared.common import Item
from shared.player_map import MoveType, ItemActionType, StateChange


class CommandQueue:
    def is_empty(self):
        pass

    def pop(self):
        pass

    def put(self, element):
        pass


class CommandSender:
    def __init__(self, queue: CommandQueue):
        self.__queue = queue

    def put(self, element):
        self.__queue.put(element)


class CommandReceiver:
    def __init__(self, queue: CommandQueue):
        self.__queue = queue

    def is_empty(self):
        return self.__queue.is_empty()

    def pop(self):
        return self.__queue.pop()


class CommandQueueCreator:
    def __init__(self, queue: CommandQueue):
        self.__queue = queue

    def get_sender(self):
        return CommandSender(self.__queue)

    def get_receiver(self):
        return CommandReceiver(self.__queue)


class LocalQueue(CommandQueue):
    def __init__(self):
        self.__queue = queue.Queue()

    def pop(self):
        self.__queue.get()

    def is_empty(self):
        return self.__queue.empty()

    def put(self, element):
        self.__queue.put(element)


class Command(ABC):
    """
        Abstract class for commands between ui and controller
    """


class ChangeState(Command):
    """
        Send controller user move
    """

    def __init__(self, change: StateChange):
        self.change = change


class AskMap(Command):
    """
        Asking controller about map
    """


class AskItemsList(Command):
    """
        Asking controller about items list
    """
