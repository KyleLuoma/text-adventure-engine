
class InputTranslator:

    def __init__(self):
        pass

    def translate(self, input_string) -> str:
        return input_string
    


class GPTInputTranslator(InputTranslator):
    import openai
    import json
    def __init__(self):
        self.openai_info = self._load_openai_info()
        super().__init__()

    def translate(self, input_string) -> str:
        prompt = self._get_prompt(input_string)
        response = self.openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user", 
                    "content": prompt}
            ],
            temperature=1,
            max_tokens=16,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"]
        )
        return response.choices[0]['message']['content'].strip()
    
    def _get_prompt(self, input_string) -> str:
        prompt_file = open("./assets/prompts/fewshot_translate_user_input.txt")
        prompt = prompt_file.read()
        prompt_file.close()
        prompt = prompt.replace("__USER_INPUT__", input_string)
        return prompt
    
    def _load_openai_info(self) -> dict:
        f = open(".local/openai.json", "r")
        openai_info = self.json.load(f)
        f.close()
        self.openai.api_key = openai_info['api_key']
        return openai_info
                                    