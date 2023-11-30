from flask import Flask, request, jsonify, render_template
from app.question_answerer import QuestionAnswerer
from app.ObjectPositionTracker import find_changes, read_and_update_json, print_object_history
from dotenv import load_dotenv
import datetime
import json
import time
import os
import threading

load_dotenv("config.env")
secret_key = os.getenv("API_KEY")



app = Flask(__name__)
question_answerer = QuestionAnswerer(secret_key)

# Data variable to store objects and their descriptions
json_data = {}
object_history = {}
    

@app.route("/")
def home():

    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get("question", "")
    answer = question_answerer.answer_question(question, json_data)
    print(answer)
    print(f'Question: {question}')
    # Logic to process the question would go here
    # For now, just returning the question as a placeholder
    return jsonify({"answer": f"{answer}"})

if __name__ == '__main__':
    # Start the background thread for updating JSON data
    
    # Här laddas directory för JSON filen så att det ska fungera på flera datorer.
    # Denna lösning ska eliminera behovet av att hårdkoda en filaddress
    base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    json_filepath = os.path.join(base_directory, "SCENE_INTERPRETER",'UE', 'scene_interpreter', 'Saved', 'MyActors.json')
    threading.Thread(target=read_and_update_json, args=(json_filepath,), daemon=True).start()
    
    # Start the Flask application
    app.run(debug=False)
