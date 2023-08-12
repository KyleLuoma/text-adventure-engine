
class Player:

    from .item import Item

    interaction_commands = [
        'get', 'drop'
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

    def add_to_inventory(self, item) -> bool:
        if len(self.inventory) < self.inventory_capacity:
            self.inventory.append(item)
            item.update_location("in your inventory")
            return True
        else:
            print("Your inventory is full.")
            return False
        
    def drop_item_by_name(self, item_name) -> Item:
        dropped_items = []
        for item in self.inventory:
            if item_name == item.name:
                self.inventory.remove(item)
                item.update_location("on the ground")
                dropped_items.append(item)
        return dropped_items
        
    def print_inventory(self) -> None:
        print("You are carrying:")
        for item in self.inventory:
            print("    -", item.name)
        print("{count} items / {capacity} capacity".format(
            count = len(self.inventory),
            capacity = self.inventory_capacity
            ))
        
    def get_inventory_drop_commands(self) -> list:
        drop_commands = []
        for item in self.inventory:
            drop_commands.append(
                "drop " + item.name
            )
        return drop_commands