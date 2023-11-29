from flask import Flask, request, jsonify, render_template
from app.question_answerer import QuestionAnswerer
#from autogen import update_JSON
from dotenv import load_dotenv
import json
import threading
import time
import os

load_dotenv("config.env")
secret_key = os.getenv("API_KEY")



app = Flask(__name__)
question_answerer = QuestionAnswerer(secret_key)

# Data variable to store objects and their descriptions
json_data = {}

# updated_json_data kommer senare användas för att lagra den uppdaterade versionen av JSON
# som består av semantic beskrivningen. Just nu används den inte eftersom den funktionen inte
# implementerats än.
updated_json_data = {}


def read_and_update_json(file_path):
    global json_data
    while True:
        try:
            with open(file_path, 'r') as file:
                new_data = json.load(file)
                if new_data != json_data:
                    json_data = new_data
                else:
                    break  # Break if data is up to date
        except Exception as e:
            print(f"Error reading JSON file: {e}")
        time.sleep(5)  # Update interval, change as needed

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
    json_filepath = os.path.join(base_directory, 'UE', 'scene_interpreter', 'Saved', 'MyActors.json')
    threading.Thread(target=read_and_update_json, args=(json_filepath,), daemon=True).start()
    
    # Start the Flask application
    app.run(debug=True)
