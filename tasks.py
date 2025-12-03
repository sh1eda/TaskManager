import json
import os
import datetime
file_path = "./data/tasks.json"

def create_task():

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                tasks = json.load(f)
            except json.JSONDecodeError:
                tasks = []
    else:
        tasks = []

    task_data = input("Enter the task name: ")
    task_desc = input("Enter a description: ")
    task_category = input("Enter a category: ")
    task_priority = input("Enter a priority (1-5): ")
    dues = input("Enter due date (YYYY-MM-DD): ")
    dues = str(datetime.datetime.strptime(dues, "%Y-%m-%d").date())
    today = str(datetime.date.today())
    task_id = len(tasks) + 1
    if not task_data:
        print("Task name cannot be empty.")
        return
    if not task_desc:
        task_desc = "No description provided."
    if not task_category:
        task_category = "Uncategorized"
    if not task_priority:
        print("Task priority cannot be empty.")
        return
    if not task_priority.isdigit():
        print("Task priority must be a number.")
        return
    if 1 <= int(task_priority) <= 5:
        task_priority = int(task_priority)
    else:
        print("Task priority must be between 1 and 5.")
    task_data = {"id": task_id, "task": task_data, "description": task_desc, "category": task_category, "priority": task_priority, "due": dues, "created": today, "updated": today, "status": "Pending..."}
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
        print("Task file not found.")
        tasks = []

    if not tasks:
        print("No task data found.")
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
                print("Error: Invalid JSON format.")
                tasks = []
    else:
        print("Task file not found.")
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
def update_task():
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                tasks = json.load(f)
            except json.JSONDecodeError:
                tasks = []
    else:
        print("Task file not found.")
        tasks = []

    if not tasks:
        print("No task data found.")
    else:
        for index, task in enumerate(tasks, start=1):
            name = task.get("task", "Unknown Task")
            status = task.get("status", "No status")
            print(f"[{index}] {name} (Status: {status})")

    task_input = input("\nEnter the number of the task to update:")
    new_status = input("\nEnter the new status: ")
    if not new_status:
        print("Status cannot be empty.")
    elif task_input.strip():
        try:
            update_index = int(task_input) - 1
            if 0 <= update_index < len(tasks):
                updated_task = tasks[update_index]
                old_status = updated_task.get("status")
                updated_task["updated"] = str(datetime.date.today())
                updated_task["status"] = new_status
                print(f"--- Task: '{updated_task.get('task')}' Updated. (Old: {old_status} -> New: {new_status}) ---")
                with open(file_path, "w") as f:
                    json.dump(tasks, f, indent=4)
                print("Saved data to file successfully.")

            else:
                print(f"ERROR: There is no task numbered {task_input}. (Enter between 1 and {len(tasks)})")

        except ValueError:
            print("Error: Enter a valid number.")
    else:
        print("Cancelled deletion operation. No changes were made to the list.")
