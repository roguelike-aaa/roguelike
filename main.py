import argparse

from consoleUI.ConsoleUI import ConsoleUI
from controller.map_controller import MapController
from shared.player_map import PlayerToken, GameSettings


def main():
    parser = argparse.ArgumentParser(description="Roguelike application")
    parser.add_argument("--width", "-y", help="Map width", required=True, type=int)
    parser.add_argument("--height", "-x", help="Map height", required=True, type=int)
    parser.add_argument("--token", "-t", help="Player username", required=True)

    args = parser.parse_args()
    controller = MapController(PlayerToken(args.token), GameSettings(args.height, args.width))
    ui = ConsoleUI(PlayerToken(args.token), controller)
    for line in controller.get_player_map(PlayerToken(args.token)).map:
        for c in line:
            print(c, end='')
        print()

    ui.start()


if __name__ == "__main__":
    main()
