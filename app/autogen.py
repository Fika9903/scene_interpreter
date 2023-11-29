import autogen
import os
import json
from dotenv import load_dotenv


load_dotenv("config.env")
secret_key = os.getenv("API_KEY")

with open('web/scene.json', 'r') as file:
    scene_data = json.load(file)

config_list = [
    {
        #  Dessa är för att köra lokal LLM
        # "api_type": "open_ai",
        # "api_base": "http://http://192.168.1.65:7860/v1",
        "model": "gpt-3.5-turbo",
        "api_key": secret_key
    }
]

llm_config={
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0
}

assistant = autogen.AssistantAgent(
    name="assistant",
    system_message="""Reply in the following format:
    1. *Figure out how to solve the task at hand, as if you're thinking out loud*
    2. Respond with the solution in the form of a Python script. Including the entirety of the script from beginning to end.
    """,
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction. 
    Otherwise, reply with the reason why the task is not solved yet."""
)

tasklist = [
    f"""
File (named 'scene.json'):
{scene_data}

Given the Scene description provided in JSON format, your task is to analyze the description and determine the relative positions of the objects within the environment. Think out loud as you process the information and make sense of where each object is placed in the room.
For example: 
    Semantic: "to the right of object X, in the middle of the room."
Once you have determined the positions, please add a 'semantic' tag after the coordinates in the JSON scene. Then, respond with a Python script that includes the updated JSON data, including the added semantic tags for each object. Replace 'json_data' in the script with the modified JSON scene.

```python
import json

json_data = # the entire modified version of the received JSON file, including your added semantic tags for each object.

# Write the updated JSON data back to the file
with open('scene.json', 'w') as file:
    json.dump(json_data, file, indent=4)
```

Please ensure that the Python script accurately reflects the changes made to the JSON scene and includes the necessary formatting to write the updated data back to the 'scene.json' file."""]

task = tasklist[0]
# task_2 = tasklist[1]
# task_3 = tasklist[2]

user_proxy.initiate_chat(
    assistant,
    message=task
)