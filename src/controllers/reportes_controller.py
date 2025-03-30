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
        return [{"id_producto": item[0], "nombre": item[1], "stock": item[2]} for item in inventory_data]

    def get_devoluciones_data(self):
        query = """
            SELECT ID_Devolucion, ID_Ticket, ID_Producto, Cantidad, Motivo, Fecha
            FROM Devolucion
        """
        return self.db.fetch_query(query)

    def get_profit_data(self):
        # Total ingresos de ventas
        query_revenue = "SELECT SUM(Total) FROM Ticket"
        revenue_result = self.db.fetch_query(query_revenue)
        revenue = revenue_result[0][0] if revenue_result and revenue_result[0][0] else 0

        # Total de devoluciones, calculado multiplicando cantidad por Precio_Publico
        query_devolutions = """
            SELECT SUM(D.Cantidad * P.Precio_Publico)
            FROM Devolucion D
            JOIN Producto P ON D.ID_Producto = P.ID_Producto
        """
        devolutions_result = self.db.fetch_query(query_devolutions)
        devolutions = devolutions_result[0][0] if devolutions_result and devolutions_result[0][0] else 0

        net_profit = revenue - devolutions
        return {"revenue": revenue, "devolutions": devolutions, "net_profit": net_profit}

    def get_sales_by_day(self):
        query = """
            SELECT DATE(Fecha_Hora) as fecha, SUM(Total) as total
            FROM Ticket
            GROUP BY DATE(Fecha_Hora)
            ORDER BY fecha ASC
        """
        results = self.db.fetch_query(query)
        return [{"fecha": row[0], "total": row[1]} for row in results]

    def get_top_products(self):
        query = """
            SELECT P.Nombre, SUM(DT.Cantidad) as cantidad
            FROM Detalle_Ticket DT
            JOIN Producto P ON DT.ID_Producto = P.ID_Producto
            GROUP BY DT.ID_Producto, P.Nombre
            ORDER BY cantidad DESC
            LIMIT 5
        """
        results = self.db.fetch_query(query)
        return [{"nombre": row[0], "cantidad": row[1]} for row in results]

    def get_low_stock_products(self, threshold=10):
        query = """
            SELECT ID_Producto, Nombre, Stock
            FROM Producto
            WHERE Stock < %s
        """
        results = self.db.fetch_query(query, (threshold,))
        return [{"id_producto": row[0], "nombre": row[1], "stock": row[2]} for row in results]

    def get_rentability_by_product(self):
        # Se asume que en Producto_Proveedor se tiene al menos un registro por producto.
        query = """
            SELECT P.ID_Producto, P.Nombre, PP.Precio_Compra, P.Precio_Publico,
                   (P.Precio_Publico - PP.Precio_Compra) AS Ganancia
            FROM Producto P
            JOIN Producto_Proveedor PP ON P.ID_Producto = PP.ID_Producto
        """
        results = self.db.fetch_query(query)
        return [{"id_producto": row[0],
                 "nombre": row[1],
                 "precio_compra": row[2],
                 "precio_publico": row[3],
                 "ganancia": row[4]} for row in results]

    def close(self):
        self.db.close()
