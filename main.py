# main.py
import sys
import tkinter as tk
from cli import start_cli
from gui import TodoApp

def start_gui():
    root = tk.Tk()
    TodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    if "--cli" in sys.argv:
        start_cli()
    else:
        start_gui()