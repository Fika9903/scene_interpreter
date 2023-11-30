from flask import Flask, request, jsonify, render_template
from app.question_answerer import QuestionAnswerer
#from autogen import update_JSON
from dotenv import load_dotenv
import datetime
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
object_history = {}

def find_changes(new_data, old_data):
    changed_items = []

    # Check if old_data is empty, then all new_data items are changes
    if not old_data:
        return new_data

    # Create a mapping of the old data for quick lookup
    old_data_mapping = {item['Name']: item for item in old_data}

    for new_item in new_data:
        name = new_item['Name']
        # Check if the item exists in old data and if it has changed
        if name not in old_data_mapping or new_item != old_data_mapping[name]:
            changed_items.append(new_item)

    return changed_items

def read_and_update_json(file_path):
    global json_data
    while True:
        try:
            with open(file_path, 'r') as file:
                new_data = json.load(file)
                if new_data != json_data:
                    changes = find_changes(new_data,json_data)
                    json_data = new_data
                    print(changes)
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    for items in changes:
                        if items['Name'] in object_history:
                            object_history[items['Name']][current_time] = items['Location']
                            print_object_history(items['Name'])
                        else:
                            object_history[items['Name']] = {current_time:items['Location']}
                else:
                    print("No new data, closing shop!")
        except Exception as e:
            print(f"Error reading JSON file: {e}")
        time.sleep(5)  # Update interval, change as needed

def print_object_history(object_name):
    object = object_history[object_name]
    print(object) 
    

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
