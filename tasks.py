import json
import os
file_path = "./data/tasks.json"

def create_task():
    task_data = input("Enter the task name: ")
    task_status = input("Enter the task status (Done/Pending): ")
    task_data = {"task": task_data, "status": task_status}
    if not os.path.exists(file_path):
        ext_data = []
    else:
        try:
            with open(file_path, "r") as f:
                ext_data = json.load(f)
        except json.JSONDecodeError:
            ext_data = []

    ext_data.append(task_data)

    with open(file_path, "w") as f:
        json.dump(ext_data, f, indent=4)

    print("Task created successfully!")
    return ext_data

def view_tasks():
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                tasks = json.load(f)
            except json.JSONDecodeError:
                tasks = []
    else:
        tasks = []

    if not tasks:
        print("There is no task yet to delete.")
    else:
        print(f"There is currently ({len(tasks)} tasks):")
        for index, task in enumerate(tasks, start=1):
            name = task.get("task", "Unknown Task")
            status = task.get("status", "No status")
            print(f"[{index}] {name} (Status: {status})")

def del_task():
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                tasks = json.load(f)
            except json.JSONDecodeError:
                tasks = []
    else:
        tasks = []

    if not tasks:
        print("There is no task yet to delete.")
    else:
        print(f"There is currently ({len(tasks)} tasks):")
        for index, task in enumerate(tasks, start=1):
            name = task.get("task", "Unknown Task")
            status = task.get("status", "No status")
            print(f"[{index}] {name} (Status: {status})")

        task_input = input("\nEnter the number of the task to delete. (Enter to cancel): ")

        if task_input.strip():
            try:
                delete_index = int(task_input) - 1
                if 0 <= delete_index < len(tasks):
                    deleted_task = tasks.pop(delete_index)
                    print(f"--- '{deleted_task.get('task')}' Removed From the List. ---")
                    with open(file_path, "w") as f:
                        json.dump(tasks, f, indent=4)
                    print("Saved data to file successfully.")

                else:
                    print(f"ERROR: There is no task numbered {task_input}. (Enter between 1 and {len(tasks)})")

            except ValueError:
                print("Error: Enter a valid number.")
        else:
            print("Cancelled deletion operation. No changes were made to the list.")