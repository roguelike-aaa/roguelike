class PlayerMap:
    def __init__(self, player_map, player):
        self.map = player_map
        self.player = player


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0


class PlayerToken:
    def __init__(self, name):
        self.name = name
