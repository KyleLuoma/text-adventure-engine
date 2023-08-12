import database.db_connector.db_connector
from game_objects.navigator import Navigator
from game_objects.player import Player
from game_objects.scene import Scene
from llm.input_translator import *


def main():
    exit = False
    db_connection = database.db_connector.db_connector.sqlite_connector("./assets/game_db/game.sqlite")
    nav = Navigator()
    player = Player()
    translator = GPTInputTranslator()
    while not exit:
        exit = gameloop(nav, player, translator)
        

def gameloop(
        nav: Navigator,
        player: Player,
        translator: GPTInputTranslator
) -> bool:
    exit = False
    current_scene = nav.get_scene(player.current_scene_id)
    print(current_scene.describe())
    user_input = input(">")
    valid_commands = current_scene.get_valid_commands()
    valid_commands += (", " + ", ".join(player.player_commands))
    valid_commands += (", " + ", ".join(player.get_inventory_drop_commands()))
    translated_input = translator.translate(
        user_input,
        valid_commands,
        nav.get_scene(player.current_scene_id).describe()
        )
    print(translated_input)
    input_list = translated_input.split(' ')
    
    if (
        translated_input in valid_commands 
        and input_list[0] in nav.movement_commands
        ):
        player.current_scene_id = current_scene.path_lookup[translated_input]['goes_to']
    
    elif (
        translated_input in valid_commands 
        and input_list[0] in player.interaction_commands
        ):
        handle_interaction_commands(input_list, player, current_scene)
    
    elif (
        translated_input in valid_commands 
        and input_list[0] in player.player_commands
        ):
        if input_list[0] == 'inventory':
            player.print_inventory()
    
    elif user_input == "exit":
        exit = True
    
    else:
        print("I don't understand that command.")
    return exit


def handle_interaction_commands(
        input_list: list,
        player: Player,
        current_scene: Scene
        ) -> None:
    if input_list[0] == 'get':
        item_list = current_scene.get_items_by_name(input_list[1])
        if len(item_list) > 0:
            for item in item_list:
                added = player.add_to_inventory(item)
                if added:
                    del current_scene.items[item.id]
        else:
            print("That item is not here.")
    if input_list[0] == 'drop' and len(input_list) > 1:
        dropped_items = player.drop_item_by_name(input_list[1])
        current_scene.add_items_to_scene(dropped_items)



if __name__ == '__main__':
    main()
