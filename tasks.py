import json
import os

def create_task(task_data: dict):
    file_path = "./data/tasks.json"
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
    file_path = "./data/tasks.json"
    with open(file_path, "r") as f:
        tasks = json.load(f)
        for index, task in enumerate(tasks, start=1):
            name = task.get("task", "Unknown Task")
            status = task.get("status", "Not Started")
            print(f"Task - {index}: {name}, Task Status: {status}")