import database.db_connector.db_connector
from game_objects.navigator import Navigator
from game_objects.player import Player
from llm.input_translator import *

def main():
    exit = False
    db_connection = database.db_connector.db_connector.sqlite_connector("./assets/game_db/game.sqlite")
    nav = Navigator()
    player = Player()
    translator = GPTInputTranslator()
    while not exit:
        print(nav.get_scene(player.current_scene_id).describe())
        user_input = input(">")
        valid_commands = nav.get_scene(
            player.current_scene_id
            ).get_valid_commands()
        translated_input = translator.translate(
            user_input,
            valid_commands,
            nav.get_scene(player.current_scene_id).describe()
            )
        print(translated_input)
        if translated_input in nav.movement_commands:
            player.current_scene_id = nav.get_scene(
                player.current_scene_id
                ).path_lookup[translated_input]['goes_to']
        elif user_input == "exit":
            exit = True
        else:
            print("I don't understand that command.")
        

if __name__ == '__main__':
    main()
