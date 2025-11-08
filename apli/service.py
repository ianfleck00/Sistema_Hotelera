from model.database import DatabaseManager
from model.cliente import cliente
from model.habitacion import habitacion
from model.reserva import reserva
import hashlib, os, binascii
from datetime import datetime

db = DatabaseManager()

# ---------- Función para obtener el próximo ID disponible ----------
def get_next_id(tabla):
    q = f"""
    SELECT MIN(t1.id + 1) AS next_id
    FROM {tabla} t1
    LEFT JOIN {tabla} t2 ON t1.id + 1 = t2.id
    WHERE t2.id IS NULL
    """
    row = db.fetchone(q)
    return row[0] if row and row[0] else 1

# ---------- USUARIOS ----------
def autenticar_usuario(username, password):
    q = "SELECT id, username, password FROM usuarios WHERE username = %s"
    row = db.fetchone(q, (username,))
    if not row:
        return False
    return row[2] == password

def crear_usuario(username, password):
    # Verificar si existe
    q = "SELECT id FROM usuarios WHERE username = %s"
    if db.fetchone(q, (username,)):
        return False
    q = "INSERT INTO usuarios (username, password) VALUES (%s, %s)"
    db.execute(q, (username, password))
    return True

# ---------- CLIENTES ----------
def obtener_clientes():
    return db.fetchall("SELECT * FROM clientes")

def agregar_cliente(nombre, apellido, email, telefono):
    cliente_id = get_next_id("clientes")
    q = "INSERT INTO clientes (id, nombre, apellido, email, telefono) VALUES (%s,%s,%s,%s,%s)"
    db.execute(q, (cliente_id, nombre, apellido, email, telefono))

def eliminar_cliente(cliente_id):
    db.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))

# ---------- HABITACIONES ----------
def obtener_habitaciones():
    return db.fetchall("SELECT * FROM habitaciones")

def agregar_habitacion(numero, tipo, precio):
    habitacion_id = get_next_id("habitaciones")
    q = "INSERT INTO habitaciones (id, numero, tipo, precio) VALUES (%s,%s,%s,%s)"
    db.execute(q, (habitacion_id, numero, tipo, precio))

def eliminar_habitacion(habitacion_id):
    db.execute("DELETE FROM habitaciones WHERE id = %s", (habitacion_id,))

# ---------- RESERVAS ----------
def obtener_reservas():
    q = """
    SELECT r.id, c.nombre, c.apellido, h.numero, r.fecha_entrada, r.fecha_salida
    FROM reservas r
    INNER JOIN clientes c ON r.cliente_id = c.id
    INNER JOIN habitaciones h ON r.habitacion_id = h.id
    """
    return db.fetchall(q)

def agregar_reserva(cliente_id, habitacion_id, fecha_inicio, fecha_fin):
    reserva_id = get_next_id("reservas")
    q = "INSERT INTO reservas (id, cliente_id, habitacion_id, fecha_entrada, fecha_salida) VALUES (%s,%s,%s,%s,%s)"
    db.execute(q, (reserva_id, cliente_id, habitacion_id, fecha_inicio, fecha_fin))

def eliminar_reserva(reserva_id):
    db.execute("DELETE FROM reservas WHERE id = %s", (reserva_id,))
