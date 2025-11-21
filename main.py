print("Welcome to Your Personal Task Manager\nChoose One Option to do.")
print("1. Add a new task")
print("2. View all tasks")
print("3. Delete a task")
print("4. Exit")
choice = ["New Task", "View Task", "Delete Task", "Exit"]
while True:
    try:
        userinput = int(input("Enter a number (1, 2, 3, or 4): "))
        if userinput == 4:
            print("Exiting...")
            break
        if userinput in [1, 2, 3, 4]:
            input_choice = userinput - 1
            choice = choice[input_choice]
            print("Valid input:", choice)
            break
        else:
            print("Invalid number. Try again.")
    except ValueError:
        print("Please enter a valid number.")