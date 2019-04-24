import collections
import enum
import random
import uuid
from abc import ABC

from shared import player_map
from shared.common import CellType, Coordinate
from shared.player_map import MoveType
from shared.map_init import ModMode


class Session:
    def __init__(self, players, game_map, mobs):
        self.game_content = SessionContent(game_map)
        self.units_interactor = UnitsInteractor(self.game_content)

        for player in players:
            self.game_content.add_player(PlayerState(game_map, player, self.units_interactor))

        for mob in mobs:
            self.game_content.add_mob(MobState(game_map, mob, self.units_interactor))

    def change_player_state(self, player_token, state_change):
        player = self.game_content.players_by_token[player_token]
        player.change_state(state_change)
        for mob in self.game_content.mobs.values():
            mob.act()

    def dump_map(self, mask=None):
        result_map = []
        for i in range(self.game_content.game_map.height):
            result_map.append([])
            for j in range(self.game_content.game_map.width):
                result_map[-1].append(
                    (self.game_content.game_map.get_cell(i, j)
                     if mask is None or mask[i][j]
                     else CellType.EMPTY_SPACE).value)
        for mob in self.game_content.mobs.values():
            if mask is None or mask[mob.data.coordinate.x][mob.data.coordinate.y]:
                result_map[mob.data.coordinate.x][mob.data.coordinate.y] = CellType.MOB.value
        return result_map

    def dump_players_map(self, players_token):
        return self.dump_map(self.game_content.players_by_token[players_token].mask)

    def player_status(self, player_token):
        status = self.game_content.players_by_token[player_token].status
        self.game_content.players_by_token[player_token].status = ""
        return status


class SinglePlayerSession(Session):
    def __init__(self, player_token, map_settings, mobs):
        super().__init__([player_token], map_settings, mobs)


class SessionContent:
    def __init__(self, game_map):
        self.players_by_token = {}
        self.players_by_id = {}
        self.mobs = {}
        self.game_map = game_map

    def add_player(self, player):
        self.players_by_token[player.token] = player
        self.players_by_id[player.data.unit_id] = player

    def add_mob(self, mob):
        self.mobs[mob.data.unit_id] = mob


class UnitsInteractor:
    def __init__(self, game_content: SessionContent):
        self.__game_content = game_content

    def attack(self, attacker, attack):
        unit = None
        if attack.target in self.__game_content.mobs:
            unit = self.__game_content.mobs[attack.target]
        elif attack.target in self.__game_content.players_by_id:
            unit = self.__game_content.players_by_id[attack.target]
        assert unit is not None
        unit.get_damaged(attack)
        if unit.data.fight_stats.current_health <= 0:
            if unit.data.unit_type is UnitState.UnitType.MOB:
                del self.__game_content.mobs[unit.data.unit_id]
            elif unit.data.unit_type is UnitState.UnitType.PLAYER:
                self.__game_content.players_by_id.pop(unit.data.unit_id, None)
                self.__game_content.players_by_token.pop(unit.token, None)

    def get_context(self, unit):
        mask = unit.get_visible_area()

        return MapView([MapView.MobView(mob.data.unit_id, mob.data.coordinate)
                        for mob in self.__game_content.mobs.values()
                        if mask[mob.data.coordinate.x][mob.data.coordinate.y]],
                       [MapView.PlayerView(player.data.unit_id, player.data.coordinate)
                        for player in self.__game_content.players_by_id.values()
                        if mask[player.data.coordinate.x][player.data.coordinate.y]]
                       )


class UnitState:
    class UnitType(enum.Enum):
        UNKNOWN = enum.auto()
        MOB = enum.auto()
        PLAYER = enum.auto()

    class UnitData:
        def __init__(self, game_map, unit):
            self.map = game_map
            self.coordinate = unit.coordinate
            self.unit_id = uuid.uuid4()
            self.unit_type = UnitState.UnitType.UNKNOWN
            self.fight_stats = unit.fight_stats

    def __init__(self, game_map, unit, game_interactor):
        self.data = UnitState.UnitData(game_map, unit)
        self.game_interactor = game_interactor

    move_deltas = {
        MoveType.DOWN: Coordinate(1, 0),
        MoveType.UP: Coordinate(-1, 0),
        MoveType.RIGHT: Coordinate(0, 1),
        MoveType.LEFT: Coordinate(0, -1),
        MoveType.NO: Coordinate(0, 0),
    }

    def change_state(self, state_change):
        new_coordinate = self.data.coordinate + UnitState.move_deltas[state_change.player_move.move_type]
        if self.data.map.get_cell(new_coordinate.x, new_coordinate.y) \
                in [CellType.DOOR, CellType.ROOM_SPACE, CellType.PATH]:
            context = self.game_interactor.get_context(self)
            for unit_view in context.player_views + context.mob_views:
                if new_coordinate == unit_view.coordinate:
                    self.game_interactor.attack(self, UnitState.UnitAttack(unit_view.unit_id, self.data.fight_stats.strength))
                    return
            self.data.coordinate = new_coordinate

    def get_visible_area(self):
        queue = collections.deque([self.data.coordinate])
        mask = [[0 for _ in range(self.data.map.width)] for _ in range(self.data.map.height)]
        mask[self.data.coordinate.x][self.data.coordinate.y] = 1

        deltas = [Coordinate(0, 1),
                  Coordinate(0, -1),
                  Coordinate(1, 0),
                  Coordinate(-1, 0)]

        while queue:
            coordinate = queue.pop()
            for delta in deltas:
                new_coordinate = coordinate + delta
                new_cell = self.data.map.get_cell(new_coordinate.x, new_coordinate.y)

                if new_cell in [CellType.ERROR, CellType.EMPTY_SPACE]:
                    continue
                if new_cell is CellType.ROOM_SPACE and mask[new_coordinate.x][new_coordinate.y] == 0:
                    queue.appendleft(new_coordinate)
                mask[new_coordinate.x][new_coordinate.y] = 1
        return mask

    class UnitAttack:
        def __init__(self, target, damage):
            self.target = target
            self.damage = damage
            self.confusion = random.randint(0, 1)

    def attack(self, unit_attack):
        self.game_interactor(self, unit_attack, self.data.fight_stats.strength)

    def get_damaged(self, unit_attack):
        self.data.fight_stats.current_health -= unit_attack.damage


class PlayerState(UnitState):
    def __init__(self, game_map, player, game_interactor):
        super().__init__(game_map, player, game_interactor)
        self.data.unit_type = UnitState.UnitType.PLAYER
        self.token = player.token
        self.status = ""
        self.mask = [[0 for _ in range(game_map.width)] for _ in range(game_map.height)]
        self.update_visible_area(self.get_visible_area())

    def change_state(self, state_change):
        super().change_state(state_change)
        self.update_visible_area(self.get_visible_area())

    def update_visible_area(self, another_mask):
        self.mask = [[another_mask[i][j] or self.mask[i][j]
                      for j in range(self.data.map.width)]
                     for i in range(self.data.map.height)]


class MobState(UnitState):
    def __init__(self, game_map, mob, game_interactor):
        super().__init__(game_map, mob, game_interactor)
        self.data.unit_type = UnitState.UnitType.MOB
        self.strategy = {
            ModMode.AGGRESSIVE: AggressiveStrategy,
            ModMode.PASSIVE: PassiveStrategy,
            ModMode.FRIGHTENED: FrightenedStrategy
        }[mob.mob_mode]

    def act(self):
        self.strategy.act(self, self.game_interactor.get_context(self))


class MapView:
    class UnitView:
        def __init__(self, unit_id, coordinate: Coordinate):
            self.unit_id = unit_id
            self.coordinate = coordinate

    class MobView(UnitView):
        pass

    class PlayerView(UnitView):
        pass

    def __init__(self, mobs, players):
        self.mob_views = mobs
        self.player_views = players


class MobStrategy:
    @classmethod
    def act(cls, mob, context):
        direction = None
        best_weight = None

        for delta in mob.move_deltas:
            weight = cls.action_weight(player_map.StateChange(player_map.PlayerMove(delta)), mob, context)
            if weight is None:
                continue
            if (direction is None) or (weight > best_weight):
                direction = delta
                best_weight = weight
        mob.change_state(player_map.StateChange(player_map.PlayerMove(direction)))

    WEIGHT_INFTY = 1000000000

    @classmethod
    def action_weight(cls, state_change, mob, context):
        raise NotImplementedError()


class PlayersDistanceBasedMobStrategy(MobStrategy, ABC):
    @classmethod
    def dist_weight(cls, state_change, mob, context):
        if not context.player_views:
            # No players nearby
            return 0 if state_change.player_move.move_type is MoveType.NO else None

        new_coordinate = mob.data.coordinate + mob.move_deltas[state_change.player_move.move_type]
        cell = mob.data.map.get_cell(new_coordinate.x, new_coordinate.y)
        if cell not in [CellType.PATH, CellType.DOOR, CellType.ROOM_SPACE]:
            return None
        return min([abs(player.coordinate.x - new_coordinate.x) + abs(player.coordinate.y - new_coordinate.y) + 1
                    for player in context.player_views])


class AggressiveStrategy(PlayersDistanceBasedMobStrategy):
    @classmethod
    def action_weight(cls, state_change, mob, context):
        weight = super().dist_weight(state_change, mob, context)
        return -weight if weight is not None else None


class PassiveStrategy(MobStrategy):
    @classmethod
    def action_weight(cls, state_change, mob, context):
        # Does nothing
        return 0 if state_change.player_move is MoveType.NO else -1


class FrightenedStrategy(PlayersDistanceBasedMobStrategy):
    @classmethod
    def action_weight(cls, state_change, mob, context):
        return super().dist_weight(state_change, mob, context)
