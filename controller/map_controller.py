from controller.session import Session
from shared.common import Map, CellType


class MapController:
    def __init__(self):
        """
                '  -- '
                '#*..|'
                '# -- '

                """

        self.session = Session(["pupa"], Map(3, 5, [
            [CellType.EMPTY_SPACE, CellType.EMPTY_SPACE, CellType.HORIZONTAL_WALL, CellType.HORIZONTAL_WALL, CellType.EMPTY_SPACE],
            [CellType.PATH, CellType.DOOR, CellType.ROOM_SPACE, CellType.ROOM_SPACE, CellType.HORIZONTAL_WALL],
            [CellType.PATH, CellType.EMPTY_SPACE, CellType.HORIZONTAL_WALL, CellType.HORIZONTAL_WALL, CellType.EMPTY_SPACE]
        ]))

    def get_map(self, player_token):
        return self.session.dump_players_map(player_token)

    def change_state(self, state_change, player_token):
        self.session.change_player_state(player_token, state_change)
