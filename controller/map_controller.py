from controller.session import Session
from mapgenerator.generator import generate_map
from shared.map_init import MapConfig
from shared.player_map import Player, PlayerMap, GameSettings


class MapController:

    def __init__(self, player_token, game_settings: GameSettings):
        self.start_new_game(player_token, game_settings)

    def start_new_game(self, player_token, game_settings: GameSettings):
        config = MapConfig(height=game_settings.map_height,
                           width=game_settings.map_width)
        generated_map = generate_map(config)
        self.session = Session([Player(generated_map.player_init_states.coordinate, player_token)], generated_map.map)

    def get_player_map(self, player_token):
        return PlayerMap(self.session.dump_players_map(player_token),
                         Player(self.session.players[player_token].coordinate, player_token))

    def change_state(self, state_change, player_token):
        self.session.change_player_state(player_token, state_change)
