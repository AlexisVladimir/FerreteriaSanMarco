# src/controllers/clientes_controller.py
from src.utils.db_helper import DatabaseHelper
from src.models.cliente import Cliente

class ClientesController:
    def __init__(self):
        self.db = DatabaseHelper()

    def agregar_cliente(self, nombre, contacto, direccion):
        query = "INSERT INTO cliente (Nombre, Contacto, Direccion) VALUES (%s, %s, %s)"
        params = (nombre, contacto, direccion)
        if self.db.execute_query(query, params):
            # En una implementación completa se recuperaría el ID generado.
            return Cliente(None, nombre, contacto, direccion)
        else:
            return None

    def obtener_clientes(self):
        query = "SELECT ID_Cliente, Nombre, Contacto, Direccion FROM cliente"
        data = self.db.fetch_query(query)
        return [Cliente(*item) for item in data]

    def editar_cliente(self, id_cliente, nombre, contacto, direccion):
        query = "UPDATE cliente SET Nombre=%s, Contacto=%s, Direccion=%s WHERE ID_Cliente=%s"
        params = (nombre, contacto, direccion, id_cliente)
        return self.db.execute_query(query, params)

    def eliminar_cliente(self, id_cliente):
        query = "DELETE FROM cliente WHERE ID_Cliente=%s"
        params = (id_cliente,)
        return self.db.execute_query(query, params)

    def close(self):
        self.db.close()
