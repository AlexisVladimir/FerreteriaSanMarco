# src/models/devolucion.py
class Devolucion:
    def __init__(self, id_devolucion, id_ticket, id_producto, cantidad, motivo, fecha):
        self.id_devolucion = id_devolucion
        self.id_ticket = id_ticket
        self.id_producto = id_producto
        self.cantidad = cantidad
        self.motivo = motivo
        self.fecha = fecha
