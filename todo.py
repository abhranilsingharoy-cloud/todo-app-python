import os
import json
import csv
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for Windows
init(autoreset=True)

DATA_FILE = "tasks.json"
DATE_FORMAT = "%Y-%m-%d"         # due date format
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# Color shortcuts
C_DONE = Fore.GREEN
C_WARN = Fore.YELLOW
C_ERR = Fore.RED
C_TITLE = Fore.CYAN + Style.BRIGHT
C_RESET = Style.RESET_ALL

# --- Core storage utilities -------------------------------------------------
def load_tasks():
    """Load tasks from tasks.json (returns list of dicts)."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print(C_ERR + "Failed to read tasks.json — starting with empty list." + C_RESET)
        return []

def save_tasks(tasks):
    """Save tasks list to tasks.json (pretty JSON)."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

# --- Helpers ---------------------------------------------------------------
def now_ts():
    return datetime.now().strftime(TIMESTAMP_FORMAT)

def parse_date(date_str):
    """Validate date in YYYY-MM-DD, return string if ok else None."""
    if not date_str:
        return ""
    try:
        dt = datetime.strptime(date_str, DATE_FORMAT)
        return dt.strftime(DATE_FORMAT)
    except ValueError:
        return None

def print_banner():
    print(C_TITLE + "=" * 38)
    print(C_TITLE + "      ADVANCED TO-DO LIST APP      ")
    print(C_TITLE + "=" * 38 + C_RESET)

def summary(tasks):
    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("completed"))
    pending = total - completed
    by_priority = {"High":0,"Medium":0,"Low":0}
    for t in tasks:
        p = t.get("priority","")
        if p in by_priority:
            by_priority[p] += 1
    print(C_TITLE + f"\nSummary:  Total: {total}  Completed: {completed}  Pending: {pending}" + C_RESET)
    print(f"  Priorities -> High: {by_priority['High']}  Medium: {by_priority['Medium']}  Low: {by_priority['Low']}")

def pretty_task_line(index, task):
    status = C_DONE + "✓" + C_RESET if task.get("completed") else C_ERR + "✗" + C_RESET
    priority = task.get("priority","")
    due = task.get("due_date","") or "No due"
    category = task.get("category","") or "No category"
    created = task.get("created","")
    return f"{index}. {task.get('task')}  [{status}]  Priority:{priority}  Due:{due}  Category:{category}  Created:{created}"

# --- CRUD & Features ------------------------------------------------------
def view_tasks(tasks, filtered=None):
    """Show tasks. If filtered provided, show that list instead."""
    list_to_show = filtered if filtered is not None else tasks
    if not list_to_show:
        print(C_WARN + "\nNo tasks found. Add a new task to get started!\n" + C_RESET)
        return
    print()
    print(C_TITLE + "--- Your Tasks ---" + C_RESET)
    for i, t in enumerate(list_to_show, 1):
        print(pretty_task_line(i, t))
    print(C_TITLE + "-------------------" + C_RESET)

def add_task(tasks):
    print(C_TITLE + "\nAdd a Task" + C_RESET)
    text = input("Task description: ").strip()
    if not text:
        print(C_ERR + "Task cannot be empty." + C_RESET)
        return

    # Priority
    pr = input("Priority (High / Medium / Low) [Medium]: ").strip().title()
    if pr == "":
        pr = "Medium"
    if pr not in ("High","Medium","Low"):
        print(C_WARN + "Invalid priority; defaulting to 'Medium'." + C_RESET)
        pr = "Medium"

    # Due date
    due_in = input("Due date (YYYY-MM-DD) [leave blank if none]: ").strip()
    parsed = parse_date(due_in)
    if due_in and parsed is None:
        print(C_ERR + "Invalid date format. Task not added." + C_RESET)
        return
    due_date = parsed or ""

    # Category
    cat = input("Category (Work / Personal / Shopping / Other) [Other]: ").strip().title()
    if not cat:
        cat = "Other"

    task = {
        "task": text,
        "completed": False,
        "priority": pr,
        "due_date": due_date,
        "category": cat,
        "created": now_ts()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(C_DONE + "Task added successfully." + C_RESET)

def remove_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        n = int(input("\nEnter task number to remove: "))
    except ValueError:
        print(C_ERR + "Enter a valid number." + C_RESET)
        return
    if not (1 <= n <= len(tasks)):
        print(C_ERR + "Invalid task number." + C_RESET)
        return
    removed = tasks.pop(n-1)
    save_tasks(tasks)
    print(C_DONE + f"Removed: {removed.get('task')}" + C_RESET)

def edit_task(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        n = int(input("\nEnter task number to edit: "))
    except ValueError:
        print(C_ERR + "Enter a valid number." + C_RESET)
        return
    if not (1 <= n <= len(tasks)):
        print(C_ERR + "Invalid task number." + C_RESET)
        return
    t = tasks[n-1]
    print(C_TITLE + "Leave blank to keep current value." + C_RESET)
    new_text = input(f"Task [{t['task']}]: ").strip()
    if new_text:
        t['task'] = new_text

    new_pr = input(f"Priority [{t['priority']}]: ").strip().title()
    if new_pr:
        if new_pr in ("High","Medium","Low"):
            t['priority'] = new_pr
        else:
            print(C_WARN + "Invalid priority; keeping current." + C_RESET)

    new_due = input(f"Due date [{t.get('due_date') or 'none'}] (YYYY-MM-DD): ").strip()
    if new_due:
        parsed = parse_date(new_due)
        if parsed is None:
            print(C_ERR + "Invalid date format; keeping current due date." + C_RESET)
        else:
            t['due_date'] = parsed

    new_cat = input(f"Category [{t.get('category','Other')}]: ").strip().title()
    if new_cat:
        t['category'] = new_cat

    save_tasks(tasks)
    print(C_DONE + "Task updated." + C_RESET)

def toggle_complete(tasks):
    view_tasks(tasks)
    if not tasks:
        return
    try:
        n = int(input("\nEnter task number to toggle complete: "))
    except ValueError:
        print(C_ERR + "Enter a valid number." + C_RESET)
        return
    if not (1 <= n <= len(tasks)):
        print(C_ERR + "Invalid task number." + C_RESET)
        return
    tasks[n-1]['completed'] = not tasks[n-1].get('completed', False)
    save_tasks(tasks)
    status = "completed" if tasks[n-1]['completed'] else "not completed"
    print(C_DONE + f"Task marked {status}." + C_RESET)

# --- Search & Filter ------------------------------------------------------
def filter_menu(tasks):
    print(C_TITLE + "\nFilter / Search Options" + C_RESET)
    print("1. Show completed")
    print("2. Show pending")
    print("3. By priority")
    print("4. By category")
    print("5. Due before date")
    print("6. Search by keyword")
    print("7. Show all (clear filters)")
    choice = input("Choose filter (1-7): ").strip()
    filtered = []
    if choice == "1":
        filtered = [t for t in tasks if t.get('completed')]
    elif choice == "2":
        filtered = [t for t in tasks if not t.get('completed')]
    elif choice == "3":
        p = input("Priority (High/Medium/Low): ").strip().title()
        filtered = [t for t in tasks if t.get('priority') == p]
    elif choice == "4":
        cat = input("Category: ").strip().title()
        filtered = [t for t in tasks if t.get('category','').title() == cat]
    elif choice == "5":
        date_in = input("Enter date (YYYY-MM-DD): ").strip()
        parsed = parse_date(date_in)
        if parsed is None:
            print(C_ERR + "Invalid date." + C_RESET)
            return
        filtered = [t for t in tasks if t.get('due_date') and t.get('due_date') <= parsed]
    elif choice == "6":
        kw = input("Keyword: ").strip().lower()
        filtered = [t for t in tasks if kw in t.get('task','').lower()]
    elif choice == "7":
        filtered = tasks
    else:
        print(C_ERR + "Invalid choice." + C_RESET)
        return
    view_tasks(tasks, filtered)

# --- Export / Import ------------------------------------------------------
def export_menu(tasks):
    print(C_TITLE + "\nExport Options" + C_RESET)
    print("1. Export to JSON file")
    print("2. Export to CSV file")
    choice = input("Choose (1-2): ").strip()
    if choice == "1":
        name = input("Filename (eg. export.json) [export.json]: ").strip() or "export.json"
        try:
            with open(name, "w", encoding="utf-8") as f:
                json.dump(tasks, f, ensure_ascii=False, indent=2)
            print(C_DONE + f"Exported to {name}" + C_RESET)
        except Exception as e:
            print(C_ERR + f"Failed to export: {e}" + C_RESET)
    elif choice == "2":
        name = input("Filename (eg. export.csv) [export.csv]: ").strip() or "export.csv"
        try:
            with open(name, "w", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["task","completed","priority","due_date","category","created"])
                for t in tasks:
                    writer.writerow([
                        t.get("task",""),
                        t.get("completed",False),
                        t.get("priority",""),
                        t.get("due_date",""),
                        t.get("category",""),
                        t.get("created","")
                    ])
            print(C_DONE + f"Exported to {name}" + C_RESET)
        except Exception as e:
            print(C_ERR + f"Failed to export: {e}" + C_RESET)
    else:
        print(C_ERR + "Invalid choice." + C_RESET)

# --- Menu & Main ----------------------------------------------------------
def show_menu():
    print(C_TITLE + "\n===== MENU =====" + C_RESET)
    print("1. View tasks")
    print("2. Add a task")
    print("3. Remove a task")
    print("4. Edit a task")
    print("5. Mark/Unmark complete")
    print("6. Filter / Search")
    print("7. Export tasks")
    print("8. Quit")
    print(C_TITLE + "===============\n" + C_RESET)

def main():
    tasks = load_tasks()
    while True:
        print_banner()
        summary(tasks)
        show_menu()
        choice = input("Enter choice (1-8): ").strip()
        if choice == "1":
            view_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            edit_task(tasks)
        elif choice == "5":
            toggle_complete(tasks)
        elif choice == "6":
            filter_menu(tasks)
        elif choice == "7":
            export_menu(tasks)
        elif choice == "8":
            print(C_DONE + "Goodbye!" + C_RESET)
            break
        else:
            print(C_ERR + "Invalid option. Choose 1-8." + C_RESET)
        input("\nPress Enter to continue...")  # pause between actions

if __name__ == "__main__":
    main()
