from datetime import date

class reserva:
    def __init__(self, id, cliente, habitacion, fecha_entrada, fecha_salida, total):
        self.id = id
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_entrada = fecha_entrada  
        self.fecha_salida = fecha_salida    
        self.total = total

