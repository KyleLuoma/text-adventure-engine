import database.db_connector.db_connector
from game_objects.navigator import Navigator
from game_objects.player import Player
from game_objects.scene import Scene
from llm.input_translator import *
from text_to_speech.game_narrator import GameNarratorAWS

debug = False
speech = True

def speech_print(text: str, narrator: GameNarratorAWS, speech = True) -> None:
    print(text)
    if speech:
        narrator.text_to_mp3(text)

def main():
    exit = False
    db_connection = database.db_connector.db_connector.sqlite_connector("./assets/game_db/game.sqlite")
    nav = Navigator()
    player = Player()
    translator = GPTInputTranslator()
    narrator = GameNarratorAWS()
    narration = "Welcome to the Text Adventure Engine\n\n"
    narration += nav.get_scene(player.current_scene_id).describe()
    speech_print(narration, narrator, speech)
    while not exit:
        exit = gameloop(nav, player, translator, narrator)
        

def gameloop(
        nav: Navigator,
        player: Player,
        translator: GPTInputTranslator,
        narrator: GameNarratorAWS
) -> bool:
    exit = False
    current_scene = nav.get_scene(player.current_scene_id)
    user_input = input("{}-> ".format(current_scene.title))
    
    print("")

    scene_commands = current_scene.get_valid_commands()
    player_commands = player.get_valid_commands()
    valid_commands = scene_commands + player_commands

    if debug:
        print("Valid commands:" + valid_commands)

    translated_input = translator.translate(
        user_input,
        valid_commands,
        nav.get_scene(player.current_scene_id).describe()
        )
    
    if debug:
        print(translated_input)

    input_list = translated_input.split(' ')
    
    if ( #Look for movement commands first
        translated_input in valid_commands 
        and input_list[0] in nav.movement_commands
        ):
        player.current_scene_id = current_scene.path_lookup[translated_input]['goes_to']
        current_scene = nav.get_scene(player.current_scene_id)
        speech_print(current_scene.describe(), narrator, speech)

    elif ( #Look for interaction commands (get, drop, look)
        translated_input in valid_commands 
        and input_list[0] in player.interaction_commands
        ):
        handle_interaction_commands(input_list, player, current_scene, narrator)

    elif ( #Handle non-look fixture related commands
        len(input_list) > 1 and input_list[1] in current_scene.get_fixture_list()
    ):
        speech_print(
            current_scene.do_fixture_command(translated_input),
            narrator,
            speech
        )
    
    elif ( #Look for player management commands
        translated_input in valid_commands 
        and input_list[0] in player.player_commands
        ):
        if input_list[0] == 'inventory':
            speech_print(
                player.get_inventory_string(),
                narrator,
                speech
            )
    
    elif user_input == "exit":
        exit = True
    
    else:
        speech_print(
            "I don't understand that command.",
            narrator,
            speech
            )
    return exit


def handle_interaction_commands(
        input_list: list,
        player: Player,
        current_scene: Scene,
        narrator: GameNarratorAWS,
        ) -> None:
    
    # Handle getting an item from the scene
    if input_list[0] == 'get':
        item_list = current_scene.get_items_by_name(input_list[1])
        if len(item_list) > 0:
            for item in item_list:
                added = player.add_to_inventory(item)
                if added['added'] == True:
                    del current_scene.items[item.id]
                speech_print(added['message'], narrator, speech)
        else:
            speech_print("That item is not here.", narrator, speech)

    # Handle dropping an inventory item
    if input_list[0] == 'drop' and len(input_list) > 1:
        dropped_items = player.drop_item_by_name(input_list[1])
        speech_print("You drop the {name} onto the ground.".format(name = input_list[1]), narrator, speech)
        current_scene.add_items_to_scene(dropped_items)
        
    # Handle looking at inventory items, scene items, and scene fixtures
    if input_list[0] == 'look' and len(input_list) > 1:

        if input_list[1] == 'around':
            speech_print(
                current_scene.describe(),
                narrator,
                speech
                )

        inventory_items = player.get_inventory_item_by_name(input_list[1])
        for item in inventory_items:
            speech_print("You look at the {name} you are holding.".format(
                name = item.name) + " " + item.description, 
                narrator, 
                speech
            )
            
        scene_items = current_scene.get_items_by_name(input_list[1])
        for item in scene_items:
            speech_print("You look at the {name} {location}.".format(
                name = item.name, 
                location = item.location
            ) + " " + item.description,
            narrator,
            speech
            )

        scene_fixture = current_scene.get_fixture_by_name(input_list[1])
        for interaction in scene_fixture['interactions']:
            if interaction['action'] == 'look':
                speech_print(interaction['description'], narrator, speech)
        




if __name__ == '__main__':
    main()
