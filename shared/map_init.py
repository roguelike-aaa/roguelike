class MapConfig:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class GeneratedMap:
    def __init__(self, game_map, players_init_state):
        self.map = game_map
        self.player_init_states = players_init_state


class PlayerInitState:
    def __init__(self, coordinate):
        self.coordinate = coordinate
