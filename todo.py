from datetime import datetime
from ui import colored, view_table
from utils import clear_screen


# Default categories
CATEGORIES = ["Work", "Personal", "School", "Shopping", "Health", "Finance"]

# Priority levels
PRIORITIES = ["High", "Medium", "Low"]


# ------------------------------------------------------------
# VIEW TASKS
# ------------------------------------------------------------
def view_tasks(tasks):
    clear_screen()

    if not tasks:
        print(colored("\nNo tasks found. Add one to get started!", "yellow"))
        return

    view_table(tasks)


# ------------------------------------------------------------
# ADD TASK
# ------------------------------------------------------------
def add_task(tasks):
    clear_screen()
    print(colored("\n➕ ADD NEW TASK\n", "cyan"))

    task_name = input("Task name: ").strip()
    if not task_name:
        print(colored("❌ Task name cannot be empty!", "red"))
        return

    # Choose priority
    print("\nSelect priority:")
    for i, p in enumerate(PRIORITIES, 1):
        print(f"{i}. {p}")
    p_choice = input("Enter number: ").strip()

    if p_choice not in ["1", "2", "3"]:
        print(colored("❌ Invalid priority. Defaulting to Medium.", "yellow"))
        priority = "Medium"
    else:
        priority = PRIORITIES[int(p_choice) - 1]

    # Choose category
    print("\nSelect category:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"{i}. {c}")
    c_choice = input("Enter number: ").strip()

    if c_choice not in [str(i) for i in range(1, len(CATEGORIES) + 1)]:
        print(colored("❌ Invalid category. Defaulting to Personal.", "yellow"))
        category = "Personal"
    else:
        category = CATEGORIES[int(c_choice) - 1]

    # Due date
    due_date = input("\nDue date (YYYY-MM-DD) or leave empty: ").strip()
    if due_date == "":
        due_date = "None"

    # Add task object
    tasks.append({
        "task": task_name,
        "completed": False,
        "priority": priority,
        "due_date": due_date,
        "category": category,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })

    print(colored("\n✅ Task added successfully!", "green"))


# ------------------------------------------------------------
# REMOVE TASK
# ------------------------------------------------------------
def remove_task(tasks):
    view_tasks(tasks)

    if not tasks:
        return

    try:
        num = int(input("\nEnter task number to remove: ").strip()) - 1
        if 0 <= num < len(tasks):
            removed = tasks.pop(num)
            print(colored(f"\n🗑 Removed: {removed['task']}", "green"))
        else:
            print(colored("❌ Invalid task number.", "red"))
    except:
        print(colored("❌ Enter a valid number.", "red"))


# ------------------------------------------------------------
# EDIT TASK
# ------------------------------------------------------------
def edit_task(tasks):
    view_tasks(tasks)

    if not tasks:
        return

    try:
        num = int(input("\nEnter task number to edit: ").strip()) - 1
        if not (0 <= num < len(tasks)):
            print(colored("❌ Invalid task number.", "red"))
            return
    except:
        print(colored("❌ Enter a valid number.", "red"))
        return

    task = tasks[num]
    print(colored("\n✏ Editing Task:\n", "cyan"))

    new_name = input(f"New name ({task['task']}): ").strip()
    if new_name:
        task["task"] = new_name

    new_due = input(f"New due date ({task['due_date']}): ").strip()
    if new_due:
        task["due_date"] = new_due

    print("\nSelect new category:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"{i}. {c}")
    new_cat = input("Category number: ").strip()
    if new_cat.isdigit() and 1 <= int(new_cat) <= len(CATEGORIES):
        task["category"] = CATEGORIES[int(new_cat)-1]

    print("\nSelect priority:")
    for i, p in enumerate(PRIORITIES, 1):
        print(f"{i}. {p}")
    new_pri = input("Priority number: ").strip()
    if new_pri.isdigit() and 1 <= int(new_pri) <= len(PRIORITIES):
        task["priority"] = PRIORITIES[int(new_pri)-1]

    print(colored("\n✅ Task updated!", "green"))


# ------------------------------------------------------------
# TOGGLE DONE / UNDONE
# ------------------------------------------------------------
def toggle_task(tasks):
    view_tasks(tasks)

    if not tasks:
        return

    try:
        num = int(input("\nEnter task number to mark done/undone: ").strip()) - 1
        if 0 <= num < len(tasks):
            tasks[num]["completed"] = not tasks[num]["completed"]
            status = "completed" if tasks[num]["completed"] else "pending"
            print(colored(f"\n✔ Task set to {status}!", "green"))
        else:
            print(colored("❌ Invalid task number.", "red"))
    except:
        print(colored("❌ Enter a valid number.", "red"))


# ------------------------------------------------------------
# SEARCH TASKS
# ------------------------------------------------------------
def search_tasks(tasks):
    keyword = input("\n🔍 Enter keyword to search: ").strip().lower()

    results = [t for t in tasks if keyword in t["task"].lower()]

    if not results:
        print(colored("\n❌ No matching tasks found.", "red"))
        return

    clear_screen()
    print(colored("\n🔍 Search Results:\n", "cyan"))
    view_table(results)


# ------------------------------------------------------------
# SORT OPTIONS
# ------------------------------------------------------------
def sort_tasks(tasks):
    print("\n🔃 Sort by:")
    print("1. Priority")
    print("2. Due date")
    print("3. Completed first")
    print("4. Alphabetical (A-Z)")
    print("5. Creation time")

    choice = input("\nChoose option: ").strip()

    if choice == "1":
        tasks.sort(key=lambda x: ["High", "Medium", "Low"].index(x["priority"]))

    elif choice == "2":
        tasks.sort(key=lambda x: x["due_date"] if x["due_date"] != "None" else "9999")

    elif choice == "3":
        tasks.sort(key=lambda x: not x["completed"])

    elif choice == "4":
        tasks.sort(key=lambda x: x["task"].lower())

    elif choice == "5":
        tasks.sort(key=lambda x: x["created"])

    else:
        print(colored("❌ Invalid sorting option.", "red"))
        return

    print(colored("\n✅ Tasks sorted successfully!", "green"))
