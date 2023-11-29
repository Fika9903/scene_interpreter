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
updated_json_data = {}

def read_and_update_json():
    global json_data
    while True:
        try:
            with open('data.json', 'r') as file:
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
    threading.Thread(target=read_and_update_json, daemon=True).start()
    
    # Start the Flask application
    app.run(debug=True)
