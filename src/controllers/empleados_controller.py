# src/controllers/empleados_controller.py
from src.models.empleado import Empleado
from src.utils.db_helper import DatabaseHelper
from src.utils.password_helper import generar_hash

class EmpleadosController:
    def __init__(self):
        self.db = DatabaseHelper()

    def agregar_empleado(self, nombre_completo, cargo, telefono, correo, fecha_ingreso, contrasena):
        hashed_pass = generar_hash(contrasena)
        query = """
            INSERT INTO empleado (Nombre_Completo, Cargo, Telefono, Correo, Fecha_Ingreso, Contrasena)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (nombre_completo, cargo, telefono, correo, fecha_ingreso, hashed_pass)
        if self.db.execute_query(query, params):
            # Se podría recuperar el ID autogenerado; aquí se retorna None para el ID.
            return Empleado(None, nombre_completo, cargo, telefono, correo, fecha_ingreso, hashed_pass)
        else:
            return None

    def obtener_empleados(self):
        query = "SELECT ID_Empleado, Nombre_Completo, Cargo, Telefono, Correo, Fecha_Ingreso, Contrasena FROM empleado"
        data = self.db.fetch_query(query)
        return [Empleado(*item) for item in data]

    def editar_empleado(self, id_empleado, nombre_completo, cargo, telefono, correo, fecha_ingreso, contrasena=None):
        if contrasena and contrasena.strip():
            # Si se proporciona nueva contraseña, se genera el hash
            hashed_pass = generar_hash(contrasena)
            query = """
                UPDATE empleado 
                SET Nombre_Completo=%s, Cargo=%s, Telefono=%s, Correo=%s, Fecha_Ingreso=%s, Contrasena=%s 
                WHERE ID_Empleado=%s
            """
            params = (nombre_completo, cargo, telefono, correo, fecha_ingreso, hashed_pass, id_empleado)
        else:
            query = """
                UPDATE empleado 
                SET Nombre_Completo=%s, Cargo=%s, Telefono=%s, Correo=%s, Fecha_Ingreso=%s 
                WHERE ID_Empleado=%s
            """
            params = (nombre_completo, cargo, telefono, correo, fecha_ingreso, id_empleado)
        return self.db.execute_query(query, params)

    def eliminar_empleado(self, id_empleado):
        query = "DELETE FROM empleado WHERE ID_Empleado=%s"
        params = (id_empleado,)
        return self.db.execute_query(query, params)

    def close(self):
        self.db.close()
