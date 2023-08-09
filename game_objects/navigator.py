from .scene import *
import os
import json

class Navigator:

    movement_commands = [
        "north", "south", "east", "west", "up", "down", "to_door"
    ]

    def __init__(self) -> None:
        self.scenes = self._load_scenes()
        self.current_level = list(self.scenes.keys())[0]

    def _load_scenes(self) -> dict:
        levels = {}
        for file in os.listdir("./assets/scenes"):
            if file.endswith(".json"):
                levels[file.replace(".json", "")] = {}
        for level in levels:
            with open("./assets/scenes/" + level + ".json", "r") as file:
                scenes_json = json.load(file)
                for scene_json in scenes_json:
                    levels[level][int(scene_json['id'])] = Scene(scene_json)
        return levels

    def get_scene(self, scene_id) -> Scene:
        return self.scenes[self.current_level][scene_id]