import json

class Item:

    next_item_id = 1

    def __init__(self, item_type_id) -> None:
        self.type_id = item_type_id
        self.id = Item.next_item_id
        Item.next_item_id += 1
        item_dict = self._load_item(item_type_id)
        self.name = item_dict['name']
        self.description = item_dict['description']
        self.size = item_dict['size']
        self.weight = item_dict['weight']
        self.location = "on the ground"


    def _load_item(self, item_type_id) -> dict:
        with open("./assets/items/" + str(item_type_id) + ".json", "r") as file:
            item_dict = json.load(file)
        return item_dict
    
    def update_location(self, location) -> None:
        self.location = location

    def get_name(self):
        return self.name