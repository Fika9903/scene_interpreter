## scene_processor.py
import json

class SceneProcessor:
    def __init__(self):
        self.scene = {}

    def process_scene(self, scene_description: str) -> dict:
        """
        Process the scene description into a dictionary.

        :param scene_description: The scene description in string format.
        :return: The scene description in dictionary format.
        """
        try:
            self.scene = json.loads(scene_description)
        except json.JSONDecodeError:
            raise ValueError("Invalid scene description. Please provide a valid JSON string.")
        return self.scene
