class Scene:

    from .item import Item
    import json

    def __init__(self, scene_dict) -> None:
        self.id = scene_dict['id']
        self.title = scene_dict['title']
        self.full_description = scene_dict['full_description']
        self.paths = scene_dict['paths']
        self.path_lookup = {}
        for path in self.paths:
            self.path_lookup[path['direction_strict']] = path
        self.items = self._process_items(scene_dict)
        pass

    def __str__(self) -> str:
        return self.title
    
    def _process_items(self, scene_dict) -> Item:
        processed_items = {}
        if 'items' in scene_dict.keys():
            scene_items = scene_dict['items']
        else:
            return {}
        for scene_item in scene_items:
            item = self.Item(scene_item['item_type_id'])
            if 'location' in scene_item.keys():
                item.update_location(scene_item['location'])
            processed_items[item.id] = item
        return processed_items

    def describe(self) -> str:
        description_string = self.title + ":\n"
        description_string += self.full_description + "\n"
        for path in self.paths:
            description_string += path['direction_description'] + " "
            description_string += path['description'] + " "
        for k in self.items.keys():
            description_string += "There is a "
            description_string += self.items[k].name + " "
            description_string += self.items[k].location + "."
        return description_string
    
    def get_valid_commands(self) -> str:
        valid_commands = []
        for path in self.paths:
            valid_commands.append(path['direction_strict'])
        if len(self.items) > 0:
            for k in self.items.keys():
                valid_commands.append("get " + self.items[k].name)
        return ", ".join(valid_commands)
    
    def get_items_by_name(self, item_name) -> list:
        item_list = []
        for k in self.items.keys():
            if self.items[k].name == item_name:
                item_list.append(self.items[k])
        return item_list
    
    def add_items_to_scene(self, item_list) -> None:
        for item in item_list:
            self.items[item.id] = item
    
