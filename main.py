## main.py
from flask import Flask, request, jsonify, render_template
from app.scene_processor import SceneProcessor
from app.object_recognizer import ObjectRecognizer
from app.question_answerer import QuestionAnswerer
from app.scene_updater import SceneUpdater
from config import debug
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv("config.env")
secret_key = os.getenv("API_KEY")

class Main:
    def __init__(self):
        self.app = Flask(__name__)
        self.scene_description = ""
        self.scene_processor = SceneProcessor()
        self.object_recognizer = ObjectRecognizer()
        self.question_answerer = QuestionAnswerer(secret_key)
        self.scene_updater = SceneUpdater()
        self.scene = {}
        
        @self.app.route("/")
        def home():
            return render_template("index.html")

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
        self.app.run(host="0.0.0.0", port=5000, debug=debug)

if __name__ == "__main__":
    main = Main()
    main.run()
