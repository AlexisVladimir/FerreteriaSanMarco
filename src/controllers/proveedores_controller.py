# src/controllers/proveedores_controller.py
from src.models.proveedor import Proveedor
from src.utils.db_helper import DatabaseHelper

class ProveedoresController:
    def __init__(self):
        self.db = DatabaseHelper()

    def agregar_proveedor(self, nombre, contacto, telefono, email, direccion):
        query = """
            INSERT INTO proveedor (Nombre, Contacto, Telefono, Email, Direccion)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (nombre, contacto, telefono, email, direccion)
        if self.db.execute_query(query, params):
            # Como ID_Proveedor es autoincrement, se retorna el objeto sin ID asignado
            return Proveedor(None, nombre, contacto, telefono, email, direccion)
        else:
            return None

    def obtener_proveedores(self):
        query = """
            SELECT ID_Proveedor, Nombre, Contacto, Telefono, Email, Direccion
            FROM proveedor
        """
        data = self.db.fetch_query(query)
        return [Proveedor(*item) for item in data]

    def editar_proveedor(self, id_proveedor, nombre, contacto, telefono, email, direccion):
        query = """
            UPDATE proveedor
            SET Nombre=%s, Contacto=%s, Telefono=%s, Email=%s, Direccion=%s
            WHERE ID_Proveedor=%s
        """
        params = (nombre, contacto, telefono, email, direccion, id_proveedor)
        return self.db.execute_query(query, params)

    def eliminar_proveedor(self, id_proveedor):
        query = "DELETE FROM proveedor WHERE ID_Proveedor=%s"
        params = (id_proveedor,)
        return self.db.execute_query(query, params)

    def close(self):
        self.db.close()
