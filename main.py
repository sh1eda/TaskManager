import tasks

task_choice = {
    "1": tasks.create_task,
    "2": tasks.view_tasks,
    "3": tasks.del_task,
    "4": tasks.update_task,
    "5": exit
}

while True:
    try:
        print("Welcome to Your Personal Task Manager\nChoose One Option to do.")
        print("1. Add a new task")
        print("2. View all tasks")
        print("3. Delete a task")
        print("4. Update a task")
        print("5. Exit")
        userinput = input("Enter a number (1, 2, 3, 4 or 5): ")

        if userinput in task_choice:
            func = task_choice[userinput]
            func()
        else:
            print("Invalid number. Try again.")
    except ValueError:
        print("Please enter a valid number.")