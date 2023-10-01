## main.py
from flask import Flask, request, jsonify, send_from_directory
from scene_processor import SceneProcessor
from object_recognizer import ObjectRecognizer
from question_answerer import QuestionAnswerer
from scene_updater import SceneUpdater
import threading
import time
import os

class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.scene_description = ""
        self.scene_processor = SceneProcessor()
        self.object_recognizer = ObjectRecognizer()
        self.question_answerer = QuestionAnswerer("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")
        self.scene_updater = SceneUpdater()
        self.scene = {}
        
        @self.app.route("/")
        def home():
            return send_from_directory('C:\\Users\\fkdah\\Desktop\\AI projekt\\MetaGPT\\workspace\\scene_interpreter\\scene_interpreter\\website', 'index.html')

        @self.app.route("/interpret", methods=["POST"])
        def interpret():
            self.scene_description = request.json.get("scene_description", "")
            self.scene = self.scene_processor.process_scene(self.scene_description)
            return jsonify({"scene": self.scene})

        @self.app.route("/ask", methods=["POST"])
        def ask():
            question = request.json.get("question", "")
            answer = self.question_answerer.answer_question(question, self.scene)
            return jsonify({"answer": answer})

    def run(self):
        def update_scene():
            while True:
                self.scene = self.object_recognizer.recognize_objects(self.scene)
                self.scene = self.scene_updater.update_scene(self.scene)
                time.sleep(5)

        threading.Thread(target=update_scene).start()
        self.app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    main = Main()
    main.run()
