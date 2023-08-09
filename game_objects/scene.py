
class Scene:

    def __init__(self, scene_dict) -> None:
        self.id = scene_dict['id']
        self.title = scene_dict['title']
        self.full_description = scene_dict['full_description']
        self.paths = scene_dict['paths']
        self.path_lookup = {}
        for path in self.paths:
            self.path_lookup[path['direction_strict']] = path
        pass

    def __str__(self) -> str:
        return self.title
    
    def describe(self) -> str:
        description_string = self.title + ":\n"
        description_string += self.full_description + "\n"
        for path in self.paths:
            description_string += path['direction_description'] + " "
            description_string += path['description'] + " "
        return description_string