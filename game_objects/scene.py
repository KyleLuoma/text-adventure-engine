

class Scene:

    from .scene_path import Path
    from .item import Item
    import json

    def __init__(self, scene_dict) -> None:
        self.id = scene_dict['id']
        self.title = scene_dict['title']
        self.full_description = scene_dict['full_description']
        self.items = self._process_items(scene_dict)
        self.paths = self._process_paths(scene_dict)
        self.fixtures = scene_dict['fixtures']
        self.fixture_commands = self._get_fixture_commands(scene_dict)
        pass

    def __str__(self) -> str:
        return self.title
    
    # Return a dict of Paths with direction_strict as key
    def _process_paths(self, scene_dict) -> dict:
        processed_paths = {}
        if 'paths' in scene_dict.keys():
            scene_paths = scene_dict['paths']
        else:
            return {}
        for path in scene_paths:
            if 'requirements' in path:
                requirements = path['requirements']
            else:
                requirements = None
            if 'fixtures' in scene_dict:
                fixtures = scene_dict['fixtures']
            else:
                fixtures = None
            path_obj = self.Path(
                path['direction_strict'],
                path['goes_to'],
                path['direction_description'],
                path['description'],
                fixtures,
                requirements
            )
            processed_paths[path_obj.direction_strict] = path_obj
        return processed_paths
    
    def _update_paths(self) -> None:
        for path in self.paths:
            self.paths[path].refresh_states()
    
    # Returns a list of paths. Must provide a state. 
    # State must be one of values in Path.requirement_types
    def get_paths_by_state(self, state) -> list:
        self._update_paths()
        if state not in self.Path.requirement_types:
            return []
        path_list = []
        for path in self.paths:
            # print(self.paths[path].description, self.paths[path].states)
            if self.paths[path].states[state] == True:
                path_list.append(self.paths[path])
        return path_list
    
        
    def _process_items(self, scene_dict) -> dict:
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
       
    def _get_fixture_commands(self, scene_dict) -> list:
        if 'fixtures' not in scene_dict.keys():
            return []
        fixtures = scene_dict['fixtures']
        commands = []
        for fixture in fixtures:
            for interaction in fixture['interactions']:
                commands.append(interaction['action'] + ' ' + fixture['title'])
        return commands
    
    def get_fixture_list(self) -> list:
        fixture_list = []
        for f in self.fixtures:
            fixture_list.append(f['title'])
        return fixture_list

    def do_fixture_command(self, command) -> str:
        command_list = command.split(" ")
        if len(command_list) != 2:
            return ""
        object = command_list[1]
        action = command_list[0]
        for f in self.fixtures:
            if f['title'] == object:
                for a in f['interactions']:
                    if a['action'] == action and 'description' in a.keys():
                        return a['description']
                    elif a['action'] == action and 'descriptions' in a.keys():
                        description = a['descriptions'][f['state']]
                        self.update_fixture_state(f['title'], a['new_state'])
                        return description
        return ""
    
    def get_fixture_by_name(self, name):
        fixture = {'interactions':[{'action':''}]}
        for f in self.fixtures:
            if f['title'] == name:
                fixture = f
        return fixture
    
    def update_fixture_state(self, fixture_title, new_state):
        for f in self.fixtures:
            if f['title'] == fixture_title:
                f['state'] = new_state

    def describe(self) -> str:
        # description_string = self.title + ":\n"
        description_string = self.full_description + "\n"
        # Parse the discription and replace fixture tags <F> with appropriate
        # values in the description.
        fixtures_list = description_string.split("<F")
        for temp in fixtures_list:
            if '</F>' in temp:
                temp = temp.split('</F>')[0]
                temp = temp.split('>')
                fixture = temp[0].strip()
                property = temp[1]
                description_string = description_string.replace(
                    '<F {fixture}>{property}</F>'.format(
                        fixture = fixture,
                        property = property 
                    ),
                    self.get_fixture_by_name(fixture)[property]
                )
        for path in self.get_paths_by_state('visible'):
            description_string += path.direction_description + " "
            description_string += path.description + " "
        for k in self.items.keys():
            description_string += "There is a "
            description_string += self.items[k].name + " "
            description_string += self.items[k].location + "."
        return description_string
    
    def get_valid_commands(self) -> str:
        valid_commands = []

        # Get path commands, check if requirements met (fixture states)
        for path in self.get_paths_by_state('passable'):
            valid_commands.append(path.direction_strict)
                    
        if len(self.items) > 0:
            for k in self.items.keys():
                valid_commands.append("get " + self.items[k].name)
                valid_commands.append("look " + self.items[k].name)
        valid_commands.append("look around")
        valid_commands += self.fixture_commands
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
    
