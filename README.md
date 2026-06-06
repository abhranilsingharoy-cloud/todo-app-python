# 📝 Terminal To-Do List App (Python)

Welcome to my Python To-Do List! I built this project as a beginner to practice Python file handling, control flow, and building interactive command-line interfaces (CLIs). 

Despite being a beginner project, I've designed it to be robust, clean, and entirely self-contained. It features a polished terminal UI with colored text, dynamic screen clearing, and secure UTF-8 file handling to ensure your data is stored safely without any external dependencies.

## 🚀 Features

- **Interactive CLI:** A clean, screen-clearing interface that feels like a modern terminal app.
- **Colored Status Indicators:** Uses ANSI escape sequences to display tasks with vivid colors.
- **Robust Storage:** Automatically saves tasks to a local `tasks.txt` file using UTF-8 encoding.
- **Full CRUD Support:** Add, view, edit, remove, and toggle the completion status of your tasks.
- **Zero Dependencies:** Built entirely using Python's standard library. No `pip install` required!

## 📦 Requirements

- Python 3.x
- Any terminal (Windows Command Prompt, PowerShell, macOS Terminal, or Linux shell).

## ▶️ How to Run

1. Clone or download this repository.
2. Open your terminal and navigate to the project folder.
3. Run the application:
   ```bash
   python todo.py
   ```

## 📁 Task Storage

Your tasks are stored locally in `tasks.txt` using the following data structure:
```text
Buy groceries|0   # 0 means incomplete  
Read a book|1     # 1 means completed
```

## 🧩 What I Learned

Building this project taught me:
- How to persistently read and write text files in Python.
- Parsing strings and handling potential data edge-cases cleanly.
- Using ANSI escape codes for coloring standard terminal output.
- Creating a continuous loop menu for CLI applications.

---

*Thank you for checking out my project! Feedback and contributions are always welcome as I continue my Python programming journey.*
