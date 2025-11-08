import tkinter as tk
from tkinter import messagebox
from apli import service

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")
        self.on_success = on_success

        tk.Label(root, text="Usuario:").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)

        tk.Label(root, text="Contraseña:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Login", command=self.login).pack(pady=10)
        tk.Button(root, text="Crear usuario", command=self.create_user).pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if service.autenticar_usuario(username, password):
            self.root.destroy()
            self.on_success()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def create_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            service.crear_usuario(username, password)
            messagebox.showinfo("Éxito", "Usuario creado correctamente")
        else:
            messagebox.showwarning("Atención", "Ingrese usuario y contraseña")
