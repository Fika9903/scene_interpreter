import os
import cv2
from pytorchyolo import detect, models

class ObjectRecognizer:
    def __init__(self):
        # Define the weights and config file paths relative to the project root
        weights_path = os.path.join(os.getcwd(), 'weights', 'yolov4.weights')
        config_path = os.path.join(os.getcwd(), 'weights', 'yolov4.cfg')

        # Load the YOLO network using OpenCV's DNN module
        #self.net = cv2.dnn.readNet(weights_path, config_path)

    def recognize_objects(self, scene: dict) -> dict:
        """
        Recognize objects in the scene using YOLOv4.

        :param scene: The scene description in dictionary format.
        :return: The scene description with recognized objects in dictionary format.
        """
        for obj in scene.get('objects', []):
            image_path = obj.get('image_path')
            if image_path:
                try:
                    img = cv2.imread(image_path)
                except Exception as e:
                    raise Exception(f"Failed to read image file at {image_path}. Please check the file path.") from e
                boxes = detect.detect_image(self.yolo, img)
                obj['recognized_objects'] = [box['class'] for box in boxes]
        return scene
