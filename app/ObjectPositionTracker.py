import json
import datetime

def read_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

def update_object_positions(objects, tracking_dict, current_time):
    for obj in objects:
        name = obj['Name']
        # Round the coordinates to one decimal place
        position = (round(obj['Location']['X'], 1), round(obj['Location']['Y'], 1), round(obj['Location']['Z'], 1))

        if name not in tracking_dict:
            tracking_dict[name] = [(current_time, position)]
        else:
            last_position = tracking_dict[name][-1][1]
            if position != last_position:
                tracking_dict[name].append((current_time, position))


def get_object_history(object_name, tracking_dict):
    return tracking_dict.get(object_name, None)

def main(json_file_path):
    object_tracking_dict = {}
    while True:
        objects = read_json_file(json_file_path)
        if objects is None:
            break

        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        update_object_positions(objects, object_tracking_dict, current_time)

        # Add a delay or trigger for the next update here
        # For demonstration, we'll just break out of the loop
        break

    print("Tracking Data:")
    for obj, positions in object_tracking_dict.items():
        print(f"{obj}: {positions}")
    
    while True:
        query = input("Enter the name of an object to get its history or type 'exit' to quit: ")
        if query.lower() == 'exit':
            break

        history = get_object_history(query, object_tracking_dict)
        if history:
            print(f"History of '{query}': {history}")
        else:
            print(f"No history found for '{query}'.")

# Set the path to your JSON file
if __name__ == '__main__':
    json_file_path = 'app/data.json'
    main(json_file_path)
    main(json_file_path)
    main(json_file_path)
    main(json_file_path)













