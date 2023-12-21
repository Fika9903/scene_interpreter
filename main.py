from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv
import openai
import os
import datetime
import json
import time
import threading

load_dotenv("config.env")
secret_key = os.getenv("API_KEY")

app = Flask(__name__)
app.secret_key = 'your_secret_key'

json_data = [] # Lagrar en direkt kopia av UE:s genererade lista av Objekt samt dess beskrivningar
object_history = {} # Lagrar en historik av objektens position under olika klockslag. Uppdateras när ett objekt rör sig.

@app.before_request
def make_session_permanent():
    session.permanent = True


@app.route("/")
def home():
    session['conversation_history'] = [] # Lagrar konversationer i en cookie, finns det inte genereras en tom lista i kakan!
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    print(session['conversation_history'])
    question = request.json.get("question", "")
    answer = answer_question(question, json_data, object_history)
    print(f'Question: {question}')
    print(answer)
    print(session['conversation_history'])
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

                # else:
                #     print("JSON is up to date.")

        except Exception as e:
            print(f"Error reading JSON file: {e}")

        time.sleep(1)  # Update interval, change as needed


# def print_object_history(arguments_json):
#         global object_history
#         arguments = json.loads(arguments_json)
#         object_name = arguments["object_name"]

#         if object_name in object_history:
#             return json.dumps({"history": object_history[object_name]})
#         else:
#             return json.dumps({"error": "Object not found"})
def print_object_history(arguments_json):
    global object_history
    arguments = json.loads(arguments_json)
    object_names = arguments["object_name"]
    history_data = {}

    for name in object_names:
        if name in object_history:
            history_data[name] = object_history[name]
        else:
            history_data[name] = "Object not found"

    return json.dumps({"history": history_data})


# def format_history(data_json):
#     # Parse the JSON string back into a dictionary
#     data = json.loads(data_json)

#     formatted_output = []
#     header = "Object Name\tTime\t\tX Coordinate\tY Coordinate\tZ Coordinate\n" + "-"*80
#     formatted_output.append(header)

#     for object_name, timestamps in data['history'].items():
#         # Check if timestamps is a dictionary (valid data) or a string (error message)
#         if isinstance(timestamps, dict):
#             for time, coordinates in timestamps.items():
#                 row = f"{object_name}\t{time}\t{coordinates['X']}\t{coordinates['Y']}\t{coordinates['Z']}"
#                 formatted_output.append(row)
#         else:
#             # Handling the case where the object history is not found
#             formatted_output.append(f"{object_name}: {timestamps}")

#     return "\n".join(formatted_output)

def format_history(data_json):
    # Parse the JSON string back into a dictionary
    data = json.loads(data_json)

    formatted_output = []
    header = "Object Name       Time        X Coordinate    Y Coordinate    Z Coordinate"
    separator = "-" * len(header)
    formatted_output.append(header)
    formatted_output.append(separator)

    for object_name, timestamps in data['history'].items():
        if isinstance(timestamps, dict):
            for time, coordinates in timestamps.items():
                formatted_output.append(
                    f"{object_name:<15} {time:<10} "
                    f"{coordinates['X']:>14,.1f} "
                    f"{coordinates['Y']:>14,.1f} "
                    f"{coordinates['Z']:>14,.1f}"
                )
        else:
            formatted_output.append(f"{object_name:<15} {timestamps}")

        # Add a separator between different objects for clarity
        formatted_output.append(separator)

    return "\n".join(formatted_output)




def answer_question(question: str, scene, object_history) -> str:
    scene_context = json.dumps(scene)
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

    
    function_description = [
        {
            "name": "print_object_history",
            "description": "Retrieve and return the historical data for a list of specified objects.",
            "parameters": {
                "type": "object",
                "properties": {
                    "object_name": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "A list of names of the objects for which to retrieve historical data."
                    }
                },
                "required": ["object_name"]
            }
        }
    ]


    if session['conversation_history'] == []:
        print('empty list, appending system message and scene context.')
        session['conversation_history'].append({"role": "system", "content": "Your job is to examine a Scene description given in JSON format and answer a question given regarding the scene. If you use the history tool, answer the question by interpreting the historical coordinates and try to understand how the objects have moved in reality rather than explaining in terms of coordinates."})
        session['conversation_history'].append({"role": "user", "content": scene_context})

    session['conversation_history'].append({"role": "user", "content": question})

    # Make the API call
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=session['conversation_history'],
        functions=function_description,
        function_call="auto"
    )

    response_message = response.choices[0].message
    print(response_message)

    # Check for function_call in the response
    if 'function_call' in response_message:
        # Extract object name and call the function
        object_name = eval(response_message['function_call']['arguments']).get("object_name")
        function_args = {"object_history": object_history, "object_name": object_name}
        function_args_json = json.dumps(function_args)
        function_response = print_object_history(arguments_json=function_args_json)
        reformated = format_history(function_response)
        # Append the function response to the conversation history
        session['conversation_history'].append({"role": "function", "name": "print_object_history", "content": reformated})
        session['conversation_history'].append({"role": "user", "content": })
        
        # Make the second API call if needed
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=session['conversation_history']
        )
        
        second_response_message = second_response.choices[0].message
        print(second_response_message)
        second_response_message = second_response.choices[0].message.content.strip()
        session['conversation_history'].append({"role": "assistant", "content": second_response_message})
        session.modified = True  # Mark session as modified
        return second_response_message
    else:
        # For non-function-call responses, append the assistant's message and return
        session['conversation_history'].append({"role": "assistant", "content": response_message['content']})
        session.modified = True  # Mark session as modified
        return response_message['content']



if __name__ == '__main__':
    # Start the background thread for updating JSON data
    
    # Här laddas directory för JSON filen så att det ska fungera på flera datorer.
    # Denna lösning ska eliminera behovet av att hårdkoda en filaddress
    base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    json_filepath = os.path.join(base_directory, "SCENE_INTERPRETER",'UE', 'scene_interpreter', 'Saved', 'MyActors.json')
    threading.Thread(target=read_and_update_json, args=(json_filepath,), daemon=True).start()
    
    # Start the Flask application
    app.run(debug=False)
