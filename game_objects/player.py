
class Player:

    from .item import Item

    interaction_commands = [
        'get', 'drop', 'look'
    ]

    player_commands = [
        'inventory'
    ]

    def __init__(
            self,
            inventory_capacity = 12,
            current_scene_id = 1
            ) -> None:
        self.inventory = []
        self.inventory_capacity = inventory_capacity
        self.current_scene_id = current_scene_id
        self.inventory_type = "bag"

    def add_to_inventory(self, item) -> dict:
        ret_dict = {
            'added': False,
            'message': ''
        }
        if len(self.inventory) < self.inventory_capacity:
            self.inventory.append(item)
            item.update_location("in your inventory")
            ret_dict['message'] = "You pick up the {item_name} and place it in your {inv_type}".format(
                    item_name = item.name,
                    inv_type = self.inventory_type
                )
            ret_dict['added'] = True
        else:
            ret_dict['message'] = "Your inventory is full."

        return ret_dict
        
    def drop_item_by_name(self, item_name) -> Item:
        dropped_items = []
        for item in self.inventory:
            if item_name == item.name:
                self.inventory.remove(item)
                item.update_location("on the ground")
                dropped_items.append(item)
        return dropped_items
        
    def get_inventory_string(self) -> None:
        inv_str = ""
        inv_str += "You are carrying:\n"
        for item in self.inventory:
            inv_str += ("    - " + item.name + "\n")
        inv_str += "You have space for:\n"
        inv_str += "{count} total items out of a capacity of {capacity}".format(
            count = len(self.inventory),
            capacity = self.inventory_capacity
            )
        return inv_str
        
    def get_inventory_interaction_commands(self) -> list:
        interaction_types = ['drop', 'look']
        interaction_commands = []
        for type in interaction_types:
            for item in self.inventory:
                interaction_commands.append(
                    type + " " + item.name
                )
        return interaction_commands
    
    def get_inventory_item_by_name(self, item_name) -> list:
        item_list = []
        for item in self.inventory:
            if item_name == item.name:
                item_list.append(item)
        return item_list
    
    def get_valid_commands(self):
        valid_commands = ""
        valid_commands += (", " + ", ".join(self.player_commands))
        valid_commands += (", " + ", ".join(self.get_inventory_interaction_commands()))
        return valid_commands