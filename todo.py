import os

TASKS_FILE = "tasks.txt"

def load_tasks():
    """Loads tasks from the tasks.txt file. Returns an empty list if file doesn't exist."""
    if not os.path.exists(TASKS_FILE):
        return []
    
    with open(TASKS_FILE, "r") as f:
        tasks = [line.strip() for line in f.readlines()]
    return tasks

def save_tasks(tasks):
    """Saves the current list of tasks to tasks.txt."""
    with open(TASKS_FILE, "w") as f:
        for task in tasks:
            f.write(task + "\n")

def view_tasks(tasks):
    """Displays all tasks in a numbered list."""
    if not tasks:
        print("\nYour to-do list is empty.")
    else:
        print("\n--- Your To-Do List ---")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")
        print("-----------------------")

def add_task(tasks):
    """Adds a new task to the list."""
    task = input("Enter a new task: ").strip()
    
    if not task:
        print("Task cannot be empty.")
        return
    
    tasks.append(task)
    save_tasks(tasks)
    print(f"\nTask '{task}' added successfully!")

def remove_task(tasks):
    """Removes a task by its number."""
    view_tasks(tasks)
    
    if not tasks:
        return

    try:
        task_num = int(input("Enter the task number to remove: "))
        index = task_num - 1

        if 0 <= index < len(tasks):
            removed_task = tasks.pop(index)
            save_tasks(tasks)
            print(f"\nTask '{removed_task}' removed successfully!")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def show_menu():
    """Prints the main menu."""
    print("\n===== To-Do List Menu =====")
    print("1. View tasks")
    print("2. Add a task")
    print("3. Remove a task")
    print("4. Exit")
    print("===========================")

def main():
    """Runs the application."""
    tasks = load_tasks()
    
    while True:
        show_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            remove_task(tasks)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()