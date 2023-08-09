
class Player:

    def __init__(
            self,
            inventory_capacity = 12,
            current_scene_id = 1
            ) -> None:
        self.inventory = []
        self.inventory_capacity = inventory_capacity
        self.current_scene_id = current_scene_id

