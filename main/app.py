import tkinter as tk
from main.login import LoginWindow
from main.main_window import MainWindow

def abrir_main_window():
    root2 = tk.Tk()
    MainWindow(root2)
    root2.mainloop()

def main():
    root = tk.Tk()
    login = LoginWindow(root, on_success=abrir_main_window)
    root.mainloop()
