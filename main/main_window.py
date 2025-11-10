import tkinter as tk
from tkinter import ttk, messagebox
from apli import service
from datetime import datetime

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Hotelera")
        self.root.geometry("1200x700")
        self.root.configure(bg="#ecf0f1")
        
        # Colores del tema
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2c3e50',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'bg': '#ecf0f1',
            'card': '#ffffff',
            'text': '#2c3e50',
            'text_light': '#7f8c8d'
        }
        
        # Estilo personalizado
        self.setup_styles()
        
        # Header
        self.create_header()
        
        # Tabs
        self.create_tabs()
    
    def setup_styles(self):
        """Configurar estilos personalizados para ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para Notebook (tabs)
        style.configure('TNotebook', background=self.colors['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', 
                       background=self.colors['card'],
                       foreground=self.colors['text'],
                       padding=[20, 10],
                       font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab',
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', 'white')])
        
        # Estilo para Treeview
        style.configure('Custom.Treeview',
                       background=self.colors['card'],
                       foreground=self.colors['text'],
                       rowheight=30,
                       fieldbackground=self.colors['card'],
                       font=('Segoe UI', 10))
        style.configure('Custom.Treeview.Heading',
                       background=self.colors['secondary'],
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat')
        style.map('Custom.Treeview',
                 background=[('selected', self.colors['primary'])])
    
    def create_header(self):
        """Crear encabezado de la aplicación"""
        header = tk.Frame(self.root, bg=self.colors['secondary'], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Título
        title = tk.Label(
            header,
            text="🏨 Sistema de Gestión Hotelera",
            font=("Segoe UI", 18, "bold"),
            bg=self.colors['secondary'],
            fg="white"
        )
        title.pack(side="left", padx=30, pady=20)
        
        # Fecha actual
        fecha = tk.Label(
            header,
            text=f"📅 {datetime.now().strftime('%d/%m/%Y')}",
            font=("Segoe UI", 11),
            bg=self.colors['secondary'],
            fg=self.colors['text_light']
        )
        fecha.pack(side="right", padx=30)

    def create_tabs(self):
        """Crear pestañas principales"""
        # Frame contenedor para tabs
        container = tk.Frame(self.root, bg=self.colors['bg'])
        container.pack(expand=1, fill="both", padx=20, pady=20)
        
        self.tabs = ttk.Notebook(container)
        self.tabs.pack(expand=1, fill="both")

        # Crear tabs
        self.tab_clientes = tk.Frame(self.tabs, bg=self.colors['bg'])
        self.tab_habitaciones = tk.Frame(self.tabs, bg=self.colors['bg'])
        self.tab_reservas = tk.Frame(self.tabs, bg=self.colors['bg'])

        self.tabs.add(self.tab_clientes, text="👥 Clientes")
        self.tabs.add(self.tab_habitaciones, text="🛏️ Habitaciones")
        self.tabs.add(self.tab_reservas, text="📋 Reservas")

        self.build_clients_tab()
        self.build_habitaciones_tab()
        self.build_reservas_tab()

    # ---------------- CLIENTES ----------------
    def build_clients_tab(self):
        # Frame contenedor con card style
        card = tk.Frame(self.tab_clientes, bg=self.colors['card'], relief="flat")
        card.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título de sección
        header_frame = tk.Frame(card, bg=self.colors['card'])
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(
            header_frame,
            text="Gestión de Clientes",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(side="left")
        
        # Botones
        btn_frame = tk.Frame(card, bg=self.colors['card'])
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        self.create_button(btn_frame, "➕ Agregar Cliente", self.agregar_cliente, 
                          self.colors['success']).pack(side="left", padx=5)
        self.create_button(btn_frame, "🗑️ Eliminar Cliente", self.eliminar_cliente, 
                          self.colors['danger']).pack(side="left", padx=5)
        
        # Frame para la tabla
        table_frame = tk.Frame(card, bg=self.colors['card'])
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Tabla de clientes
        columns = ("id", "nombre", "apellido", "email", "telefono")
        self.tree_clientes = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree_clientes.yview)
        
        # Configurar columnas
        column_widths = {"id": 60, "nombre": 150, "apellido": 150, "email": 200, "telefono": 120}
        for col in columns:
            self.tree_clientes.heading(col, text=col.upper())
            self.tree_clientes.column(col, width=column_widths.get(col, 120), anchor="center")
        
        self.tree_clientes.pack(fill="both", expand=True)
        self.cargar_clientes()

    def cargar_clientes(self):
        for row in self.tree_clientes.get_children():
            self.tree_clientes.delete(row)
        for cliente in service.obtener_clientes():
            self.tree_clientes.insert("", "end", values=cliente)

    def agregar_cliente(self):
        def guardar():
            if not all([entry_nombre.get(), entry_apellido.get(), entry_email.get(), entry_telefono.get()]):
                messagebox.showwarning("Atención", "Por favor complete todos los campos")
                return
            
            service.agregar_cliente(
                entry_nombre.get().strip(),
                entry_apellido.get().strip(),
                entry_email.get().strip(),
                entry_telefono.get().strip()
            )
            messagebox.showinfo("Éxito", "Cliente agregado correctamente")
            top.destroy()
            self.cargar_clientes()

        top = tk.Toplevel(self.root)
        top.title("Nuevo Cliente")
        top.geometry("400x350")
        top.configure(bg=self.colors['card'])
        top.resizable(False, False)
        
        # Centrar ventana
        self.center_window(top, 400, 350)
        
        # Frame contenedor
        form_frame = tk.Frame(top, bg=self.colors['card'])
        form_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Título
        tk.Label(
            form_frame,
            text="Nuevo Cliente",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Campos
        fields = [
            ("Nombre:", 1),
            ("Apellido:", 2),
            ("Email:", 3),
            ("Teléfono:", 4)
        ]
        
        entries = []
        for label, row in fields:
            tk.Label(
                form_frame,
                text=label,
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['card'],
                fg=self.colors['text'],
                anchor="w"
            ).grid(row=row, column=0, sticky="w", pady=5)
            
            entry = tk.Entry(
                form_frame,
                font=("Segoe UI", 10),
                bg="#f8f9fa",
                relief="flat",
                highlightthickness=1,
                highlightbackground="#dee2e6",
                highlightcolor=self.colors['primary']
            )
            entry.grid(row=row, column=1, sticky="ew", pady=5, ipady=5)
            entries.append(entry)
        
        entry_nombre, entry_apellido, entry_email, entry_telefono = entries
        
        form_frame.columnconfigure(1, weight=1)
        
        # Botones
        btn_frame = tk.Frame(form_frame, bg=self.colors['card'])
        btn_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        self.create_button(btn_frame, "💾 Guardar", guardar, self.colors['success']).pack(side="left", padx=5)
        self.create_button(btn_frame, "❌ Cancelar", top.destroy, self.colors['danger']).pack(side="left", padx=5)

    def eliminar_cliente(self):
        selected = self.tree_clientes.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un cliente para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            cliente_id = self.tree_clientes.item(selected[0])["values"][0]
            service.eliminar_cliente(cliente_id)
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            self.cargar_clientes()

    # ---------------- HABITACIONES ----------------
    def build_habitaciones_tab(self):
        card = tk.Frame(self.tab_habitaciones, bg=self.colors['card'], relief="flat")
        card.pack(fill="both", expand=True, padx=10, pady=10)
        
        header_frame = tk.Frame(card, bg=self.colors['card'])
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(
            header_frame,
            text="Gestión de Habitaciones",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(side="left")
        
        btn_frame = tk.Frame(card, bg=self.colors['card'])
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        self.create_button(btn_frame, "➕ Agregar Habitación", self.agregar_habitacion,
                          self.colors['success']).pack(side="left", padx=5)
        self.create_button(btn_frame, "🗑️ Eliminar Habitación", self.eliminar_habitacion,
                          self.colors['danger']).pack(side="left", padx=5)
        
        table_frame = tk.Frame(card, bg=self.colors['card'])
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("id", "numero", "tipo", "precio_por_noche")
        self.tree_habitaciones = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree_habitaciones.yview)
        
        column_widths = {"id": 80, "numero": 150, "tipo": 200, "precio_por_noche": 150}
        for col in columns:
            self.tree_habitaciones.heading(col, text=col.upper())
            self.tree_habitaciones.column(col, width=column_widths.get(col, 120), anchor="center")
        
        self.tree_habitaciones.pack(fill="both", expand=True)
        self.cargar_habitaciones()

    def cargar_habitaciones(self):
        for row in self.tree_habitaciones.get_children():
            self.tree_habitaciones.delete(row)
        for hab in service.obtener_habitaciones():
            self.tree_habitaciones.insert("", "end", values=hab)

    def agregar_habitacion(self):
        def guardar():
            if not all([entry_numero.get(), entry_tipo.get(), entry_precio_por_noche.get()]):
                messagebox.showwarning("Atención", "Por favor complete todos los campos")
                return
            
            try:
                float(entry_precio_por_noche.get())
            except ValueError:
                messagebox.showerror("Error", "El precio_por_noche debe ser un número válido")
                return
            
            service.agregar_habitacion(
                entry_numero.get().strip(),
                entry_tipo.get().strip(),
                entry_precio_por_noche.get().strip()
            )
            messagebox.showinfo("Éxito", "Habitación agregada correctamente")
            top.destroy()
            self.cargar_habitaciones()

        top = tk.Toplevel(self.root)
        top.title("Nueva Habitación")
        top.geometry("400x300")
        top.configure(bg=self.colors['card'])
        top.resizable(False, False)
        
        self.center_window(top, 400, 300)
        
        form_frame = tk.Frame(top, bg=self.colors['card'])
        form_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        tk.Label(
            form_frame,
            text="Nueva Habitación",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        fields = [
            ("Número:", 1),
            ("Tipo:", 2),
            ("precio:", 3)
        ]
        
        entries = []
        for label, row in fields:
            tk.Label(
                form_frame,
                text=label,
                font=("Segoe UI", 10, "bold"),
                bg=self.colors['card'],
                fg=self.colors['text'],
                anchor="w"
            ).grid(row=row, column=0, sticky="w", pady=5)
            
            entry = tk.Entry(
                form_frame,
                font=("Segoe UI", 10),
                bg="#f8f9fa",
                relief="flat",
                highlightthickness=1,
                highlightbackground="#dee2e6",
                highlightcolor=self.colors['primary']
            )
            entry.grid(row=row, column=1, sticky="ew", pady=5, ipady=5)
            entries.append(entry)
        
        entry_numero, entry_tipo, entry_precio_por_noche = entries
        form_frame.columnconfigure(1, weight=1)
        
        btn_frame = tk.Frame(form_frame, bg=self.colors['card'])
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(20, 0))
        
        self.create_button(btn_frame, "💾 Guardar", guardar, self.colors['success']).pack(side="left", padx=5)
        self.create_button(btn_frame, "❌ Cancelar", top.destroy, self.colors['danger']).pack(side="left", padx=5)

    def eliminar_habitacion(self):
        selected = self.tree_habitaciones.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione una habitación para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta habitación?"):
            hab_id = self.tree_habitaciones.item(selected[0])["values"][0]
            service.eliminar_habitacion(hab_id)
            messagebox.showinfo("Éxito", "Habitación eliminada correctamente")
            self.cargar_habitaciones()

    # ---------------- RESERVAS ----------------
    def build_reservas_tab(self):
        card = tk.Frame(self.tab_reservas, bg=self.colors['card'], relief="flat")
        card.pack(fill="both", expand=True, padx=10, pady=10)
        
        header_frame = tk.Frame(card, bg=self.colors['card'])
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        tk.Label(
            header_frame,
            text="Gestión de Reservas",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).pack(side="left")
        
        btn_frame = tk.Frame(card, bg=self.colors['card'])
        btn_frame.pack(fill="x", padx=20, pady=10)
        
        self.create_button(btn_frame, "➕ Nueva Reserva", self.agregar_reserva,
                          self.colors['success']).pack(side="left", padx=5)
        self.create_button(btn_frame, "🗑️ Cancelar Reserva", self.eliminar_reserva,
                          self.colors['danger']).pack(side="left", padx=5)
        
        table_frame = tk.Frame(card, bg=self.colors['card'])
        table_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")
        
        columns = ("id", "cliente", "apellido", "habitacion", "fecha_inicio", "fecha_fin")
        self.tree_reservas = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview",
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree_reservas.yview)
        
        column_widths = {"id": 60, "cliente": 130, "apellido": 130, "habitacion": 100, 
                        "fecha_inicio": 120, "fecha_fin": 120}
        for col in columns:
            self.tree_reservas.heading(col, text=col.upper().replace("_", " "))
            self.tree_reservas.column(col, width=column_widths.get(col, 120), anchor="center")
        
        self.tree_reservas.pack(fill="both", expand=True)
        self.cargar_reservas()

    def cargar_reservas(self):
        for row in self.tree_reservas.get_children():
            self.tree_reservas.delete(row)
        for res in service.obtener_reservas():
            self.tree_reservas.insert("", "end", values=res)

    def agregar_reserva(self):
        def guardar():
            if combo_cliente.current() == -1 or combo_hab.current() == -1:
                messagebox.showwarning("Atención", "Seleccione un cliente y una habitación")
                return
            
            if not entry_inicio.get() or not entry_fin.get():
                messagebox.showwarning("Atención", "Complete las fechas de la reserva")
                return
            
            # Validar formato de fecha
            try:
                datetime.strptime(entry_inicio.get(), '%Y-%m-%d')
                datetime.strptime(entry_fin.get(), '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Error", "Formato de fecha inválido. Use: YYYY-MM-DD")
                return
            
            resultado = service.agregar_reserva(
                cliente_id=clientes[combo_cliente.current()][0],
                habitacion_id=habitaciones[combo_hab.current()][0],
                fecha_inicio=entry_inicio.get(),
                fecha_fin=entry_fin.get()
            )
            
            if resultado:
                messagebox.showinfo("Éxito", "Reserva creada correctamente")
                top.destroy()
                self.cargar_reservas()
            else:
                messagebox.showerror(
                    "Habitación no disponible",
                    "La habitación no está disponible en las fechas seleccionadas.\n\n"
                    "Por favor elija otras fechas u otra habitación."
                )

        top = tk.Toplevel(self.root)
        top.title("Nueva Reserva")
        top.geometry("450x400")
        top.configure(bg=self.colors['card'])
        top.resizable(False, False)
        
        self.center_window(top, 450, 400)
        
        clientes = service.obtener_clientes()
        habitaciones = service.obtener_habitaciones()
        
        if not clientes or not habitaciones:
            messagebox.showwarning("Atención", "Debe tener clientes y habitaciones registrados")
            top.destroy()
            return
        
        form_frame = tk.Frame(top, bg=self.colors['card'])
        form_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        tk.Label(
            form_frame,
            text="Nueva Reserva",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text']
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Cliente
        tk.Label(
            form_frame,
            text="Cliente:",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text'],
            anchor="w"
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        combo_cliente = ttk.Combobox(
            form_frame,
            values=[f"{c[1]} {c[2]}" for c in clientes],
            font=("Segoe UI", 10),
            state="readonly"
        )
        combo_cliente.grid(row=1, column=1, sticky="ew", pady=5, ipady=5)
        
        # Habitación
        tk.Label(
            form_frame,
            text="Habitación:",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text'],
            anchor="w"
        ).grid(row=2, column=0, sticky="w", pady=5)
        
        combo_hab = ttk.Combobox(
            form_frame,
            values=[f"Hab. {h[1]} - {h[2]}" for h in habitaciones],
            font=("Segoe UI", 10),
            state="readonly"
        )
        combo_hab.grid(row=2, column=1, sticky="ew", pady=5, ipady=5)
        
        # Fecha inicio
        tk.Label(
            form_frame,
            text="Fecha Inicio:",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text'],
            anchor="w"
        ).grid(row=3, column=0, sticky="w", pady=5)
        
        entry_inicio = tk.Entry(
            form_frame,
            font=("Segoe UI", 10),
            bg="#f8f9fa",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#dee2e6",
            highlightcolor=self.colors['primary']
        )
        entry_inicio.grid(row=3, column=1, sticky="ew", pady=5, ipady=5)
        entry_inicio.insert(0, datetime.now().strftime('%Y-%m-%d'))
        
        # Fecha fin
        tk.Label(
            form_frame,
            text="Fecha Fin:",
            font=("Segoe UI", 10, "bold"),
            bg=self.colors['card'],
            fg=self.colors['text'],
            anchor="w"
        ).grid(row=4, column=0, sticky="w", pady=5)
        
        entry_fin = tk.Entry(
            form_frame,
            font=("Segoe UI", 10),
            bg="#f8f9fa",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#dee2e6",
            highlightcolor=self.colors['primary']
        )
        entry_fin.grid(row=4, column=1, sticky="ew", pady=5, ipady=5)
        
        # Nota de formato
        tk.Label(
            form_frame,
            text="Formato de fecha: YYYY-MM-DD (ej: 2024-12-25)",
            font=("Segoe UI", 8),
            bg=self.colors['card'],
            fg=self.colors['text_light']
        ).grid(row=5, column=0, columnspan=2, pady=(5, 15))
        
        form_frame.columnconfigure(1, weight=1)
        
        btn_frame = tk.Frame(form_frame, bg=self.colors['card'])
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(10, 0))
        
        self.create_button(btn_frame, "💾 Crear Reserva", guardar, self.colors['success']).pack(side="left", padx=5)
        self.create_button(btn_frame, "❌ Cancelar", top.destroy, self.colors['danger']).pack(side="left", padx=5)

    def eliminar_reserva(self):
        selected = self.tree_reservas.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione una reserva para cancelar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de cancelar esta reserva?"):
            res_id = self.tree_reservas.item(selected[0])["values"][0]
            service.eliminar_reserva(res_id)
            messagebox.showinfo("Éxito", "Reserva cancelada correctamente")
            self.cargar_reservas()
    
    # ---------------- UTILIDADES ----------------
    def create_button(self, parent, text, command, bg_color):
        """Crear botón estilizado"""
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold"),
            bg=bg_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=8,
            activebackground=self.darken_color(bg_color),
            activeforeground="white"
        )
        return btn
    
    def darken_color(self, color):
        """Oscurecer un color hex para el efecto hover"""
        colors = {
            '#3498db': '#2980b9',
            '#27ae60': '#229954',
            '#e74c3c': '#c0392b',
            '#f39c12': '#e67e22'
        }
        return colors.get(color, color)
    
    def center_window(self, window, width, height):
        """Centrar una ventana en la pantalla"""
        window.update_idletasks()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
