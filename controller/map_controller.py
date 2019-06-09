from controller.session import Session
from map.generator import generate_map
from map.saver import MapSaver
from shared.map_init import MapConfig
from shared.player_map import Player, PlayerMap, GameSettings, CurrentFightStats, Mob


class MapController:

    def __init__(self, player_token, game_settings: GameSettings):
        self.session = None
        self.start_new_game(player_token, game_settings)

    def start_new_game(self, player_token, game_settings: GameSettings):
        config = MapConfig(height=game_settings.map_height,
                           width=game_settings.map_width)
        generated_map = generate_map(config)
        player = generated_map.player_init_states
        self.session = Session([Player(player.coordinate,
                                       player_token, CurrentFightStats(player.fight_stats.health,
                                                                       player.fight_stats.strength))],
                               generated_map.map, [Mob(mob.coordinate,
                                                       mob.mob_mode,
                                                       CurrentFightStats(mob.fight_stats.health,
                                                                         mob.fight_stats.strength))
                                                   for mob in generated_map.mobs])

    def get_player_items(self, player_token):
        player = self.session.game_content.players_by_token[player_token]
        return player.data.inventory

    def get_player_map(self, player_token):
        player = self.session.game_content.players_by_token[player_token]
        return PlayerMap(self.session.dump_players_map(player_token),
                         Player(player.data.coordinate, player_token, player.data.fight_stats),
                         self.session.player_status(player_token))

    def change_state(self, state_change, player_token):
        self.session.change_player_state(player_token, state_change)

    def save_game(self):
        MapSaver().save(self.session)

    def load_game(self):
        self.session = MapSaver().load()