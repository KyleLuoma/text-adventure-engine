
class ConversationManager:

    def __init__(self, name):
        self.name = name
        pass

    def respond_to_player(self, player_input):
        return player_input
    

class GPTConversationManager(ConversationManager):
    import openai
    import json

    def __init__(self, name):
        self.openai_info = self._load_openai_info()
        super().__init__(name)


    def generate_response(
            self,
            player_input: str,
            npc_conversation_history: list,
            npc_description: str,
            npc_history_summary: str,
            player_name: str = "player",
            debug: bool = False
            ):
        
        game_instructions = {
            "role": "user", "content": "You are a non-player character in a text adventure game. Interact with the user as if they are playing the game. You shall not make reference to the game. You shall not act as an assistant. You shall act in accordance with the character traits that will be described to you. It is extremely important that the user not be made aware that this is a game."
            }
        
        messages = [
            game_instructions,
            {"role": "user", "content": npc_description}, 
            {"role": "user", "content": npc_history_summary}
            ]
        
        messages += npc_conversation_history
        messages += [{"role": "user", "content": player_input}]

        if debug:
            print(messages)

        completion = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=messages
            )
        
        npc_conversation_history += [{"role": "user", "content": player_input}]
        npc_conversation_history += [{"role": 'system', "content": completion.choices[0].message.content}]
        print(completion.choices[0].message.content)    
        return npc_conversation_history


    def _load_openai_info(self) -> dict:
        f = open(".local/openai.json", "r")
        openai_info = self.json.load(f)
        f.close()
        self.openai.api_key = openai_info['api_key']
        return openai_info
    
if __name__ == "__main__":
    cm = GPTConversationManager("Neo")
    npc_description = "You are a small bear with a red shirt. You like Honey, and you go by the name Whinnie the Pooh."
    history = []
    history_summary = "This is your first time meeting the user. The user is a player in a text adventure game. You are to interact with the user as a character in the game."
    player_name = "Christopher"
    while True:
        user_input = input(">")
        history = cm.generate_response(
            user_input, history, npc_description, 
            history_summary, 
            player_name=player_name,
            debug=False
        )
