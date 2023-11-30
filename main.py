from flask import Flask, request, jsonify, render_template
from app.question_answerer import QuestionAnswerer
from dotenv import load_dotenv
import openai
import langchain
import os
import datetime
import json
import time
import threading

load_dotenv("config.env")
secret_key = os.getenv("API_KEY")

app = Flask(__name__)
question_answerer = QuestionAnswerer(secret_key)

json_data = [] # Lagrar en direkt kopia av UE:s genererade lista av Objekt samt dess beskrivningar
object_history = {} # Lagrar en historik av objektens position under olika klockslag. Uppdateras när ett objekt rör sig.


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    question = request.json.get("question", "")
    answer = answer_question(question, json_data, object_history)
    print(f'Question: {question}')
    print(answer)
    # Logic to process the question would go here
    # For now, just returning the question as a placeholder
    return jsonify({"answer": f"{answer}"})

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
    global json_data, object_history
    while True:
        try:
            with open(file_path, 'r') as file:
                new_data = json.load(file)

                if new_data != json_data:
                    print("New data identified.")
                    changes = find_changes(new_data, json_data)
                    json_data = new_data
                    #print(json_data)
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")

                    for items in changes:
                        # Round the coordinates to one decimal place
                        rounded_location = {coord: round(items['Location'][coord], 1) for coord in ['X', 'Y', 'Z']}

                        if items['Name'] in object_history:
                            object_history[items['Name']][current_time] = rounded_location
                            print("updated object")
                        else:
                            object_history[items['Name']] = {current_time: rounded_location}
                    #print(object_history)

                else:
                    print("JSON is up to date.")

        except Exception as e:
            print(f"Error reading JSON file: {e}")

        time.sleep(1)  # Update interval, change as needed


def print_object_history(arguments_json):
        global object_history
        arguments = json.loads(arguments_json)
        object_name = arguments["object_name"]

        if object_name in object_history:
            return json.dumps({"history": object_history[object_name]})
        else:
            return json.dumps({"error": "Object not found"})


def answer_question(question: str, scene, object_history) -> str:
    scene_context = json.dumps(scene)
    object_history_json = json.dumps(object_history)

    openai.api_key = secret_key
    function_description = [
        {
            "name": "print_object_history",
            "description": "Retrieve and return the historical data of a specified object.",
            "parameters": {
                "type": "object",
                "properties": {
                    "object_name": {
                        "type": "string",
                        "description": "The name of the object for which to retrieve historical data."
                    }
                },
                "required": ["object_name"]
            }
        }
    ]

    messages = [
        {"role": "system", "content": "Your job is to examine a Scene description given in JSON format and answer a question given regarding the scene."},
        {"role": "user", "content": scene_context},
        {"role": "user", "content": question}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        #messages=[{"role": "system", "content": "Your job is to examine a Scene description given in JSON format and answer a question given regarding the scene."},
        #{"role": "user", "content": scene_context + "\n" + question}],
        functions=function_description,
        function_call="auto"
    )

    response_message = response.choices[0].message
    print(response_message)

    if 'function_call' in response_message:
        object_name = eval(response_message['function_call']['arguments']).get("object_name")
        print(object_name)

        # Prepare arguments for the print_object_history function
        function_args = {"object_history": object_history, "object_name": object_name}
        function_args_json = json.dumps(function_args)

        # Call the print_object_history function
        function_response = print_object_history(arguments_json=function_args_json)
        print(function_response)

    print(function_response)
    second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "user", "content": question},
                response_message,
                {
                "role": "function",
                "name": "print_object_history",
                "content": function_response
                },
                
            ],
        )
    
    print (second_response['choices'][0]['message']['content'])
    return second_response.choices[0].message.content.strip()


if __name__ == '__main__':
    # Start the background thread for updating JSON data
    
    # Här laddas directory för JSON filen så att det ska fungera på flera datorer.
    # Denna lösning ska eliminera behovet av att hårdkoda en filaddress
    base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    json_filepath = os.path.join(base_directory, "SCENE_INTERPRETER",'UE', 'scene_interpreter', 'Saved', 'MyActors.json')
    threading.Thread(target=read_and_update_json, args=(json_filepath,), daemon=True).start()
    
    # Start the Flask application
    app.run(debug=False)
