import enum
import uuid
from abc import ABC


class Coordinate:
    """
        Class storing a position on the map.
    """

    def __init__(self, x: int, y: int):
        """
        :param x: height coordinate.
        :param y: width coordinate.
        """
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Bonus:
    def __init__(self, health_bonus=0, strength_bonus=0):
        self.health_bonus = health_bonus
        self.strength_bonus = strength_bonus

    def __add__(self, other):
        return Bonus(self.health_bonus + other.health_bonus, self.strength_bonus + other.strength_bonus)


class ItemType(enum.Enum):
    UNKNOWN = enum.auto(),
    WEAPON = enum.auto(),
    POTION = enum.auto(),
    CLOTH = enum.auto(),


class Item(ABC):
    def __init__(self, bonus: Bonus, name: str):
        self.id = uuid.uuid4()
        self.bonus = bonus
        self.name = name
        self.item_type = ItemType.UNKNOWN


"""
    General game elements shared between all components.
"""


class Map:
    """
        Class storing map layout. Includes only elements listed in the CellType enum below.
    """

    def __init__(self, height: int, width: int, map_array):
        """
        :param height: height of the map.
        :param width: width of the map.
        :param map_array: list of height lists each containing exactly width CellType items.
        """

        self.width = width
        self.height = height
        self.map_array = map_array

    def get_cell(self, height: int, width: int):
        """
        Cell content getter.

        :param height: height coordinate of the required cell.
        :param width: width coordinate of the required cell.
        :return: content of the cell if it existed. Otherwise returns CellType.ERROR value.
        """
        return self.map_array[height][
            width] if 0 <= height < self.height and 0 <= width < self.width else CellType.ERROR


class CellType(enum.Enum):
    """
        Class describing possible map cell content.
    """
    EMPTY_SPACE = ' '
    ROOM_SPACE = '.'
    MOB = '%'
    VERTICAL_WALL = '|'
    HORIZONTAL_WALL = '-'
    DOOR = '*'
    PATH = '#'
    HERO = '@'
    ITEM = '!'
    ERROR = '倈'


from shared.player_map import Inventory


class Usable(Item, ABC):
    def use(self, inventory: Inventory):
        raise NotImplementedError()


class Wearable(Item, ABC):
    def wear(self, inventory):
        raise NotImplementedError()

    def take_off(self, inventory):
        raise NotImplementedError()


class Weapon(Wearable):
    def wear(self, inventory: Inventory):
        if inventory.active_weapon is not None:
            return False
        inventory.active_weapon = self
        return True

    def take_off(self, inventory: Inventory):
        if inventory.active_weapon is not None:
            inventory.items[self.id] = self
            inventory.active_weapon = None
            return True
        return False

    def __init__(self, bonus: Bonus, name: str):
        super().__init__(bonus, name)
        self.item_type = ItemType.WEAPON


class Potion(Item):
    def __init__(self, bonus: Bonus, name: str):
        super().__init__(bonus, name)
        self.item_type = ItemType.POTION


class Cloth(Wearable, ABC):
    def __init__(self, bonus: Bonus, name: str):
        super().__init__(bonus, name)
        self.item_type = ItemType.CLOTH


class BodyCloth(Cloth):
    def __init__(self, bonus: Bonus, name: str):
        super().__init__(bonus, name)

    def wear(self, inventory: Inventory):
        if inventory.active_shirt is not None:
            return False
        inventory.active_shirt = self
        return True

    def take_off(self, inventory: Inventory):
        if inventory.active_shirt is not None:
            inventory.items[self.id] = self
            inventory.active_shirt = None
            return True
        return False


class HeadCloth(Cloth):
    def __init__(self, bonus: Bonus, name: str):
        super().__init__(bonus, name)

    def wear(self, inventory: Inventory):
        if inventory.active_helmet is not None:
            return False
        inventory.active_helmet = self
        return True

    def take_off(self, inventory: Inventory):
        if inventory.active_helmet is not None:
            inventory.items[self.id] = self
            inventory.active_helmet = None
            return True
        return False
