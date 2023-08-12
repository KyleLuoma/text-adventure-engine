import json

class Item:

    def __init__(self, item_id) -> None:
        self.id = item_id
        item_dict = self._load_item(item_id)
        self.name = item_dict['name']
        self.description = item_dict['description']


    def _load_item(self, item_id) -> dict:
        with open("./assets/items/" + str(item_id) + ".json", "r") as file:
            item_dict = json.load(file)
        return item_dict