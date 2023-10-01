## scene_updater.py
from typing import Dict

class SceneUpdater:
    def __init__(self, update_interval: int = 5):
        self.update_interval = update_interval

    def update_scene(self, scene: Dict) -> Dict:
        """
        Update the scene with recognized objects.

        :param scene: The scene description with recognized objects in dictionary format.
        :return: The updated scene description in dictionary format.
        """
        for obj in scene.get('objects', []):
            recognized_objects = obj.get('recognized_objects', [])
            if recognized_objects:
                obj['objects'] = recognized_objects
        return scene
