class PlayerMap:
    def __init__(self, player_map, player):
        self.map = player_map
        self.player = player


class Player:
    def __init__(self, x, y, player_token):
        self.coordinate = Coordinate(x, y)
        self.token = player_token


class PlayerToken:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == self.name

    def __hash__(self):
        return self.name.__hash__()


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)
