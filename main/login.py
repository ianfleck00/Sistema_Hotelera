import tkinter as tk
from tkinter import messagebox
from apli import service

class LoginWindow:
    def __init__(self, root, on_success):
        self.root = root
        self.root.title("Sistema de Gestión Hotelera - Login")
        self.root.geometry("450x500")
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)
        self.on_success = on_success
        
        # Centrar ventana
        self.center_window()
        
        # Frame principal
        main_frame = tk.Frame(root, bg="#2c3e50")
        main_frame.pack(expand=True, fill="both", padx=40, pady=40)
        
        # Título
        title_label = tk.Label(
            main_frame, 
            text="🏨 HOTEL MANAGER", 
            font=("Segoe UI", 24, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame, 
            text="Sistema de Gestión Hotelera", 
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="#95a5a6"
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Frame para el formulario
        form_frame = tk.Frame(main_frame, bg="#34495e", relief="flat")
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Padding interno
        inner_frame = tk.Frame(form_frame, bg="#34495e")
        inner_frame.pack(padx=30, pady=30)
        
        # Usuario
        user_label = tk.Label(
            inner_frame, 
            text="Usuario", 
            font=("Segoe UI", 11, "bold"),
            bg="#34495e",
            fg="#ecf0f1",
            anchor="w"
        )
        user_label.pack(fill="x", pady=(0, 5))
        
        self.username_entry = tk.Entry(
            inner_frame,
            font=("Segoe UI", 11),
            bg="#ecf0f1",
            fg="#2c3e50",
            relief="flat",
            highlightthickness=2,
            highlightbackground="#7f8c8d",
            highlightcolor="#3498db"
        )
        self.username_entry.pack(fill="x", ipady=8, pady=(0, 20))
        self.username_entry.bind("<Return>", lambda e: self.password_entry.focus())
        
        # Contraseña
        pass_label = tk.Label(
            inner_frame, 
            text="Contraseña", 
            font=("Segoe UI", 11, "bold"),
            bg="#34495e",
            fg="#ecf0f1",
            anchor="w"
        )
        pass_label.pack(fill="x", pady=(0, 5))
        
        self.password_entry = tk.Entry(
            inner_frame,
            show="●",
            font=("Segoe UI", 11),
            bg="#ecf0f1",
            fg="#2c3e50",
            relief="flat",
            highlightthickness=2,
            highlightbackground="#7f8c8d",
            highlightcolor="#3498db"
        )
        self.password_entry.pack(fill="x", ipady=8, pady=(0, 25))
        self.password_entry.bind("<Return>", lambda e: self.login())
        
        # Botón Login
        login_btn = tk.Button(
            inner_frame,
            text="Iniciar Sesión",
            command=self.login,
            font=("Segoe UI", 11, "bold"),
            bg="#3498db",
            fg="white",
            relief="flat",
            cursor="hand2",
            activebackground="#2980b9",
            activeforeground="white"
        )
        login_btn.pack(fill="x", ipady=10, pady=(0, 10))
        
        # Botón Crear Usuario
        create_btn = tk.Button(
            inner_frame,
            text="Crear Nueva Cuenta",
            command=self.create_user,
            font=("Segoe UI", 10),
            bg="#34495e",
            fg="#3498db",
            relief="flat",
            cursor="hand2",
            activebackground="#34495e",
            activeforeground="#2980b9",
            bd=0
        )
        create_btn.pack(fill="x", ipady=5)
        
        # Footer
        footer_label = tk.Label(
            main_frame, 
            text="© 2024 Hotel Manager System", 
            font=("Segoe UI", 8),
            bg="#2c3e50",
            fg="#7f8c8d"
        )
        footer_label.pack(side="bottom", pady=(20, 0))
        
        # Enfocar en el campo de usuario
        self.username_entry.focus()
    
    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.root.update_idletasks()
        width = 450
        height = 550
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Atención", "Por favor complete todos los campos")
            return
        
        if service.autenticar_usuario(username, password):
            self.root.destroy()
            self.on_success()
        else:
            messagebox.showerror("Error de Autenticación", "Usuario o contraseña incorrectos")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def create_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Atención", "Ingrese usuario y contraseña para crear la cuenta")
            return
        
        if len(password) < 4:
            messagebox.showwarning("Atención", "La contraseña debe tener al menos 4 caracteres")
            return
        
        if service.crear_usuario(username, password):
            messagebox.showinfo("Éxito", "Usuario creado correctamente\nYa puede iniciar sesión")
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus()
        else:
            messagebox.showerror("Error", "El usuario ya existe")
