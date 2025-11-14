import os

TASKS_FILE = "tasks.txt"

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"

def load_tasks():
    """Loads tasks from tasks.txt. Format: task|completed"""
    if not os.path.exists(TASKS_FILE):
        return []

    tasks = []
    with open(TASKS_FILE, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) == 2:
                task, status = parts
                tasks.append([task, status == "1"])
            else:
                tasks.append([parts[0], False])
    return tasks

def save_tasks(tasks):
    """Saves tasks back to tasks.txt."""
    with open(TASKS_FILE, "w") as f:
        for task, completed in tasks:
            f.write(f"{task}|{'1' if completed else '0'}\n")

def view_tasks(tasks):
    """Displays all tasks with color + status."""
    if not tasks:
        print(YELLOW + "\nNo tasks found. Add a new task to get started!" + RESET)
        return
    
    print(CYAN + "\n--- Your To-Do List ---" + RESET)
    for i, (task, completed) in enumerate(tasks, 1):
        status = GREEN + "[✓ Completed]" + RESET if completed else RED + "[✗ Not Done]" + RESET
        print(f"{i}. {task} {status}")
    print(CYAN + "-----------------------" + RESET)

def add_task(tasks):
    task = input("Enter a new task: ").strip()
    if not task:
        print(RED + "Task cannot be empty." + RESET)
        return

    tasks.append([task, False])
    save_tasks(tasks)
    print(GREEN + f"\nTask '{task}' added successfully!" + RESET)

def remove_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    try:
        num = int(input("Enter task number to remove: ")) - 1
        if 0 <= num < len(tasks):
            removed = tasks.pop(num)[0]
            save_tasks(tasks)
            print(GREEN + f"\nTask '{removed}' removed!" + RESET)
        else:
            print(RED + "Invalid number." + RESET)
    except ValueError:
        print(RED + "Enter a valid number." + RESET)

def edit_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    try:
        num = int(input("Enter task number to edit: ")) - 1
        if 0 <= num < len(tasks):
            new_text = input("Enter updated task: ").strip()
            if not new_text:
                print(RED + "Task cannot be empty." + RESET)
                return
            tasks[num][0] = new_text
            save_tasks(tasks)
            print(GREEN + "\nTask updated successfully!" + RESET)
        else:
            print(RED + "Invalid number." + RESET)
    except ValueError:
        print(RED + "Enter a valid number." + RESET)

def toggle_task_completion(tasks):
    view_tasks(tasks)
    if not tasks:
        return

    try:
        num = int(input("Enter task number to toggle complete: ")) - 1
        if 0 <= num < len(tasks):
            tasks[num][1] = not tasks[num][1]
            save_tasks(tasks)
            if tasks[num][1]:
                print(GREEN + "\nTask marked as completed!" + RESET)
            else:
                print(YELLOW + "\nTask marked as not completed." + RESET)
        else:
            print(RED + "Invalid number." + RESET)
    except ValueError:
        print(RED + "Enter a valid number." + RESET)

def show_menu():
    print(BOLD + CYAN + "\n===== To-Do List Menu =====" + RESET)
    print("1. View tasks")
    print("2. Add a task")
    print("3. Remove a task")
    print("4. Edit a task")
    print("5. Mark/Unmark completed")
    print("6. Exit")
    print(BOLD + CYAN + "===========================\n" + RESET)

def main():
    tasks = load_tasks()
    
    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            remove_task(tasks)
        elif choice == '4':
            edit_task(tasks)
        elif choice == '5':
            toggle_task_completion(tasks)
        elif choice == '6':
            print(GREEN + "Goodbye!" + RESET)
            break
        else:
            print(RED + "Invalid choice. Please choose 1-6." + RESET)

if __name__ == "__main__":
    main()
