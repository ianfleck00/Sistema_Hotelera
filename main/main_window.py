import tkinter as tk
from tkinter import ttk, messagebox
from apli import service

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión Hotel")
        self.root.geometry("900x600")
        self.create_tabs()

    def create_tabs(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=1, fill="both")

        # Crear tabs
        self.tab_clientes = ttk.Frame(self.tabs)
        self.tab_habitaciones = ttk.Frame(self.tabs)
        self.tab_reservas = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_clientes, text="Clientes")
        self.tabs.add(self.tab_habitaciones, text="Habitaciones")
        self.tabs.add(self.tab_reservas, text="Reservas")

        self.build_clients_tab()
        self.build_habitaciones_tab()
        self.build_reservas_tab()

    # ---------------- CLIENTES ----------------
    def build_clients_tab(self):
        # Tabla de clientes
        columns = ("id", "nombre", "apellido", "email", "telefono")
        self.tree_clientes = ttk.Treeview(self.tab_clientes, columns=columns, show="headings")
        for col in columns:
            self.tree_clientes.heading(col, text=col.title())
            self.tree_clientes.column(col, width=120)
        self.tree_clientes.pack(fill="both", expand=True, pady=10)

        # Botones
        frame = tk.Frame(self.tab_clientes)
        frame.pack(pady=5)
        tk.Button(frame, text="Agregar Cliente", command=self.agregar_cliente).pack(side="left", padx=5)
        tk.Button(frame, text="Eliminar Cliente", command=self.eliminar_cliente).pack(side="left", padx=5)

        self.cargar_clientes()

    def cargar_clientes(self):
        for row in self.tree_clientes.get_children():
            self.tree_clientes.delete(row)
        for cliente in service.obtener_clientes():
            self.tree_clientes.insert("", "end", values=cliente)

    def agregar_cliente(self):
        def guardar():
            service.agregar_cliente(entry_nombre.get(), entry_apellido.get(),
                                    entry_email.get(), entry_telefono.get())
            top.destroy()
            self.cargar_clientes()

        top = tk.Toplevel(self.root)
        top.title("Nuevo Cliente")
        tk.Label(top, text="Nombre").grid(row=0, column=0)
        tk.Label(top, text="Apellido").grid(row=1, column=0)
        tk.Label(top, text="Email").grid(row=2, column=0)
        tk.Label(top, text="Teléfono").grid(row=3, column=0)

        entry_nombre = tk.Entry(top); entry_nombre.grid(row=0, column=1)
        entry_apellido = tk.Entry(top); entry_apellido.grid(row=1, column=1)
        entry_email = tk.Entry(top); entry_email.grid(row=2, column=1)
        entry_telefono = tk.Entry(top); entry_telefono.grid(row=3, column=1)

        tk.Button(top, text="Guardar", command=guardar).grid(row=4, column=0, columnspan=2, pady=5)

    def eliminar_cliente(self):
        selected = self.tree_clientes.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un cliente")
            return
        cliente_id = self.tree_clientes.item(selected[0])["values"][0]
        service.eliminar_cliente(cliente_id)
        self.cargar_clientes()

    # ---------------- HABITACIONES ----------------
    def build_habitaciones_tab(self):
        columns = ("id", "numero", "tipo", "precio")
        self.tree_habitaciones = ttk.Treeview(self.tab_habitaciones, columns=columns, show="headings")
        for col in columns:
            self.tree_habitaciones.heading(col, text=col.title())
            self.tree_habitaciones.column(col, width=120)
        self.tree_habitaciones.pack(fill="both", expand=True, pady=10)

        frame = tk.Frame(self.tab_habitaciones)
        frame.pack(pady=5)
        tk.Button(frame, text="Agregar Habitación", command=self.agregar_habitacion).pack(side="left", padx=5)
        tk.Button(frame, text="Eliminar Habitación", command=self.eliminar_habitacion).pack(side="left", padx=5)

        self.cargar_habitaciones()

    def cargar_habitaciones(self):
        for row in self.tree_habitaciones.get_children():
            self.tree_habitaciones.delete(row)
        for hab in service.obtener_habitaciones():
            self.tree_habitaciones.insert("", "end", values=hab)

    def agregar_habitacion(self):
        def guardar():
            service.agregar_habitacion(entry_numero.get(), entry_tipo.get(), entry_precio.get())
            top.destroy()
            self.cargar_habitaciones()

        top = tk.Toplevel(self.root)
        top.title("Nueva Habitación")
        tk.Label(top, text="Número").grid(row=0, column=0)
        tk.Label(top, text="Tipo").grid(row=1, column=0)
        tk.Label(top, text="Precio").grid(row=2, column=0)

        entry_numero = tk.Entry(top); entry_numero.grid(row=0, column=1)
        entry_tipo = tk.Entry(top); entry_tipo.grid(row=1, column=1)
        entry_precio = tk.Entry(top); entry_precio.grid(row=2, column=1)

        tk.Button(top, text="Guardar", command=guardar).grid(row=3, column=0, columnspan=2, pady=5)

    def eliminar_habitacion(self):
        selected = self.tree_habitaciones.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione una habitación")
            return
        hab_id = self.tree_habitaciones.item(selected[0])["values"][0]
        service.eliminar_habitacion(hab_id)
        self.cargar_habitaciones()

    # ---------------- RESERVAS ----------------
    def build_reservas_tab(self):
        columns = ("id", "cliente", "apellido", "habitacion", "fecha_inicio", "fecha_fin")
        self.tree_reservas = ttk.Treeview(self.tab_reservas, columns=columns, show="headings")
        for col in columns:
            self.tree_reservas.heading(col, text=col.title())
            self.tree_reservas.column(col, width=120)
        self.tree_reservas.pack(fill="both", expand=True, pady=10)

        frame = tk.Frame(self.tab_reservas)
        frame.pack(pady=5)
        tk.Button(frame, text="Agregar Reserva", command=self.agregar_reserva).pack(side="left", padx=5)
        tk.Button(frame, text="Eliminar Reserva", command=self.eliminar_reserva).pack(side="left", padx=5)

        self.cargar_reservas()

    def cargar_reservas(self):
        for row in self.tree_reservas.get_children():
            self.tree_reservas.delete(row)
        for res in service.obtener_reservas():
            self.tree_reservas.insert("", "end", values=res)

    def agregar_reserva(self):
        def guardar():
            service.agregar_reserva(
                cliente_id=clientes[combo_cliente.current()][0],
                habitacion_id=habitaciones[combo_hab.current()][0],
                fecha_inicio=entry_inicio.get(),
                fecha_fin=entry_fin.get()
            )
            top.destroy()
            self.cargar_reservas()

        top = tk.Toplevel(self.root)
        top.title("Nueva Reserva")

        clientes = service.obtener_clientes()
        habitaciones = service.obtener_habitaciones()

        tk.Label(top, text="Cliente").grid(row=0, column=0)
        tk.Label(top, text="Habitación").grid(row=1, column=0)
        tk.Label(top, text="Fecha Inicio (YYYY-MM-DD)").grid(row=2, column=0)
        tk.Label(top, text="Fecha Fin (YYYY-MM-DD)").grid(row=3, column=0)

        combo_cliente = ttk.Combobox(top, values=[f"{c[1]} {c[2]}" for c in clientes])
        combo_cliente.grid(row=0, column=1)

        combo_hab = ttk.Combobox(top, values=[f"{h[1]}" for h in habitaciones])
        combo_hab.grid(row=1, column=1)

        entry_inicio = tk.Entry(top); entry_inicio.grid(row=2, column=1)
        entry_fin = tk.Entry(top); entry_fin.grid(row=3, column=1)

        tk.Button(top, text="Guardar", command=guardar).grid(row=4, column=0, columnspan=2, pady=5)

    def eliminar_reserva(self):
        selected = self.tree_reservas.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione una reserva")
            return
        res_id = self.tree_reservas.item(selected[0])["values"][0]
        service.eliminar_reserva(res_id)
        self.cargar_reservas()
