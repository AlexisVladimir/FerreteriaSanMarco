# src/controllers/inventario_controller.py
from src.utils.db_helper import DatabaseHelper

class InventarioController:
    def __init__(self):
        self.db = DatabaseHelper()

    def agregar_producto(self, nombre, descripcion, categoria, cantidad, precio, ubicacion, proveedor, fecha):
        query = """
            INSERT INTO Producto (Nombre, Descripcion, ID_Subcategoria, Stock, Precio_Unitario, ID_Ubicacion, ID_Proveedor, Fecha_Ingreso)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        # Nota: ID_Subcategoria e ID_Proveedor deben mapearse a valores reales en la base de datos.
        # Por simplicidad, asumimos que categoria y proveedor son IDs (números).
        params = (nombre, descripcion, categoria, cantidad, precio, ubicacion, proveedor, fecha)
        return self.db.execute_query(query, params)

    def buscar_productos(self, filtro, valor):
        query = f"SELECT ID_Producto, Nombre, ID_Subcategoria, Precio_Unitario, Stock, ID_Ubicacion FROM Producto WHERE {filtro} LIKE %s"
        params = (f"%{valor}%",)
        return self.db.fetch_query(query, params)

    def buscar_por_estanteria(self, ubicacion):
        query = "SELECT ID_Producto, Nombre, ID_Subcategoria, Stock, ID_Ubicacion FROM Producto WHERE ID_Ubicacion = %s"
        params = (ubicacion,)
        return self.db.fetch_query(query, params)

    def buscar_birlos_compatibles(self, marca, modelo, anio):
        query = """
            SELECT b.ID_Birlo, b.Medida, b.Tipo_Rosca, b.Compatibilidad_Vehiculo
            FROM Birlo b
            JOIN Vehiculo v ON b.ID_Birlo = v.ID_Birlo
            WHERE v.Marca = %s AND v.Modelo = %s AND v.Año = %s
        """
        params = (marca, modelo, anio)
        return self.db.fetch_query(query, params)

    def close(self):
        self.db.close()