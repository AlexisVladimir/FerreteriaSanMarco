# src/controllers/devolucion_controller.py
from src.models.devolucion import Devolucion
from src.utils.db_helper import DatabaseHelper
from datetime import date

class DevolucionController:
    def __init__(self):
        self.db = DatabaseHelper()

    def agregar_devolucion(self, id_ticket, id_producto, cantidad, motivo, fecha=None):
        if fecha is None:
            fecha = date.today().strftime("%Y-%m-%d")
        query = """
            INSERT INTO Devolucion (ID_Ticket, ID_Producto, Cantidad, Motivo, Fecha)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (id_ticket, id_producto, cantidad, motivo, fecha)
        if self.db.execute_query(query, params):
            # Opcional: actualizar el stock en la tabla Producto
            self._actualizar_stock(id_producto, cantidad)
            return Devolucion(None, id_ticket, id_producto, cantidad, motivo, fecha)
        else:
            return None

    def _actualizar_stock(self, id_producto, cantidad):
        # Aumenta el stock del producto en la cantidad devuelta.
        query = "UPDATE Producto SET Stock = Stock + %s WHERE ID_Producto = %s"
        params = (cantidad, id_producto)
        self.db.execute_query(query, params)

    def close(self):
        self.db.close()
