# src/controllers/proveedores_controller.py
from src.models.proveedor import Proveedor
from src.utils.db_helper import DatabaseHelper

class ProveedoresController:
    def __init__(self):
        self.db = DatabaseHelper()

    def agregar_proveedor(self, nombre, contacto, telefono, email, direccion, sitio_web, notas):
        query = """
            INSERT INTO proveedor (Nombre, Contacto, Telefono, Email, Direccion, Sitio_Web, Notas)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (nombre, contacto, telefono, email, direccion, sitio_web, notas)
        if self.db.execute_query(query, params):
            # Como ID_Proveedor es autoincrement, no lo asignamos manualmente
            return Proveedor(None, nombre, contacto, telefono, email, direccion, sitio_web, notas)
        else:
            return None

    def obtener_proveedores(self):
        query = """
            SELECT ID_Proveedor, Nombre, Contacto, Telefono, Email, Direccion, Sitio_Web, Notas
            FROM proveedor
        """
        data = self.db.fetch_query(query)
        return [Proveedor(*item) for item in data]

    def editar_proveedor(self, id_proveedor, nombre, contacto, telefono, email, direccion, sitio_web, notas):
        query = """
            UPDATE proveedor
            SET Nombre=%s, Contacto=%s, Telefono=%s, Email=%s, Direccion=%s, Sitio_Web=%s, Notas=%s
            WHERE ID_Proveedor=%s
        """
        params = (nombre, contacto, telefono, email, direccion, sitio_web, notas, id_proveedor)
        return self.db.execute_query(query, params)

    def eliminar_proveedor(self, id_proveedor):
        query = "DELETE FROM proveedor WHERE ID_Proveedor=%s"
        params = (id_proveedor,)
        return self.db.execute_query(query, params)

    def close(self):
        self.db.close()
