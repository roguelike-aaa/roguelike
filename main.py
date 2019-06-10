import argparse
import threading

from consoleUI.ConsoleUI import ConsoleUI
from controller.map_controller import MapController
from shared.command import CommandQueueCreator, LocalQueue, AskMap, SendMap, AskItemsList, SendItemsList, ChangeState, \
    LoadGame, SaveGame
from shared.player_map import PlayerToken, GameSettings


def main():
    parser = argparse.ArgumentParser(description="Roguelike application")
    parser.add_argument("--width", "-y", help="Map width", required=True, type=int)
    parser.add_argument("--height", "-x", help="Map height", required=True, type=int)
    parser.add_argument("--token", "-t", help="Player username", required=True)

    args = parser.parse_args()

    controller_commands = CommandQueueCreator(LocalQueue())
    ui_commands = CommandQueueCreator(LocalQueue())

    token = PlayerToken(args.token)

    controller = MapController(token, GameSettings(args.height, args.width))

    ui = ConsoleUI(controller_commands.get_receiver(), ui_commands.get_sender())
    for line in controller.get_player_map(PlayerToken(args.token)).map:
        for c in line:
            print(c, end='')
        print()

    ui_thread = threading.Thread(target=ui.start)
    ui_thread.start()

    input_commands = ui_commands.get_receiver()
    output_commands = controller_commands.get_sender()

    while True:
        if not input_commands.is_empty():
            new_command = input_commands.pop()
            if isinstance(new_command, AskMap):
                output_commands.put(SendMap(controller.get_player_map(PlayerToken(args.token))))
                continue
            if isinstance(new_command, AskItemsList):
                output_commands.put(SendItemsList(controller.get_player_items(PlayerToken(args.token))))
                continue
            if isinstance(new_command, ChangeState):
                controller.change_state(new_command.change, token)
                continue
            if isinstance(new_command, LoadGame):
                controller.load_game()
                continue
            if isinstance(new_command, SaveGame):
                controller.save_game()
                continue


if __name__ == "__main__":
    main()
