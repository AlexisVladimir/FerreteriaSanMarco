# src/controllers/reportes_controller.py
from src.utils.db_helper import DatabaseHelper

class ReportesController:
    def __init__(self):
        self.db = DatabaseHelper()

    def get_sales_data(self):
        query = "SELECT ID_Ticket, Fecha_Hora, ID_Empleado, ID_Cliente, Total FROM Ticket"
        return self.db.fetch_query(query)

    def get_inventory_data(self):
        query = """
            SELECT ID_Producto, Nombre, Stock
            FROM Producto
        """
        inventory_data = self.db.fetch_query(query)
        # Convertir los datos a un formato de diccionario para el report_generator
        return [{"id_producto": item[0], "nombre": item[1], "stock": item[2]} for item in inventory_data]

    def close(self):
        self.db.close()