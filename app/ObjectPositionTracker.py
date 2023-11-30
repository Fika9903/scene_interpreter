
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

def read_and_update_json(file_path,json_data,object_history):
    global json_data
    while True:
        try:
            with open(file_path, 'r') as file:
                new_data = json.load(file)

                if new_data != json_data:
                    print("New data identified.")
                    changes = find_changes(new_data,json_data)
                    json_data = new_data
                    print(json_data)
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")

                    for items in changes:
                        if items['Name'] in object_history:
                            print(f'New object: {print_object_history(items['Name'])}')
                            object_history[items['Name']][current_time] = items['Location']
                        else:
                            object_history[items['Name']] = {current_time:items['Location']}

        except Exception as e:
            print(f"Error reading JSON file: {e}")

        time.sleep(5)  # Update interval, change as needed

def print_object_history(object_history, object_name):
    return object_history[object_name]
